from io import BytesIO
from pathlib import Path
import time
from typing import Any

import cv2
import numpy as np
from PIL import Image
import requests

from backend.core.config import settings


class BillScanError(RuntimeError):
    status_code = 502


class AzureConfigurationError(BillScanError):
    status_code = 503


class ImagePreprocessingError(BillScanError):
    status_code = 422


class AzureSubmissionError(BillScanError):
    status_code = 502


class AzureTimeoutError(BillScanError):
    status_code = 504


class AzureConnectionError(BillScanError):
    status_code = 502


class AzureOcrFailedError(BillScanError):
    status_code = 502


def preprocess_image(image_bytes: bytes) -> bytes:
    try:
        image = Image.open(BytesIO(image_bytes))
        image.load()
        image_array = np.array(image)
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)
        gray = cv2.medianBlur(gray, 3)
        _, thresholded = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )
        output = BytesIO()
        Image.fromarray(thresholded).save(output, format="PNG")
        return output.getvalue()
    except Exception as exc:
        raise ImagePreprocessingError(
            "Image preprocessing failed; upload a valid JPG, JPEG, or PNG image."
        ) from exc


def normalize_ocr_text(result_json: dict[str, Any]) -> str:
    ocr_text = ""
    analyze_result = result_json.get("analyzeResult", {})
    for page in analyze_result.get("readResults", []):
        for line in page.get("lines", []):
            ocr_text += line.get("text", "") + "\n"
    if not isinstance(ocr_text, str):
        ocr_text = str(ocr_text)
    return ocr_text.strip()


def _azure_url() -> str:
    endpoint = (settings.azure_vision_endpoint or "").rstrip("/")
    if not endpoint or not settings.azure_vision_key:
        raise AzureConfigurationError(
            "Azure Vision configuration is missing on the backend."
        )
    api_version = settings.azure_vision_api_version.strip("/")
    return f"{endpoint}/vision/{api_version}/read/analyze"


def scan_image(image_bytes: bytes) -> str:
    processed_bytes = preprocess_image(image_bytes)
    url = _azure_url()
    submit_headers = {
        "Ocp-Apim-Subscription-Key": settings.azure_vision_key,
        "Content-Type": "application/octet-stream",
    }

    try:
        response = requests.post(
            url,
            headers=submit_headers,
            data=processed_bytes,
            timeout=settings.azure_vision_submit_timeout_seconds,
        )
    except requests.exceptions.Timeout as exc:
        raise AzureTimeoutError("Azure OCR submission timed out.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise AzureConnectionError("Cannot reach Azure Vision API.") from exc
    except requests.exceptions.RequestException as exc:
        raise AzureSubmissionError("Azure OCR submission failed.") from exc

    if response.status_code != 202:
        raise AzureSubmissionError(
            f"Azure API Error {response.status_code}: {response.text}"
        )

    operation_url = response.headers.get("Operation-Location")
    if not operation_url:
        raise AzureSubmissionError("No Operation-Location in Azure response.")

    poll_headers = {"Ocp-Apim-Subscription-Key": settings.azure_vision_key}
    deadline = time.monotonic() + settings.azure_vision_max_poll_seconds
    attempts = 0
    while attempts < settings.azure_vision_max_poll_attempts:
        if time.monotonic() >= deadline:
            break
        try:
            result = requests.get(
                operation_url,
                headers=poll_headers,
                timeout=settings.azure_vision_poll_timeout_seconds,
            )
            result_json = result.json()
        except requests.exceptions.Timeout as exc:
            raise AzureTimeoutError("Azure OCR polling timed out.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AzureConnectionError("Cannot reach Azure Vision API while polling.") from exc
        except (requests.exceptions.RequestException, ValueError) as exc:
            raise AzureSubmissionError("Azure OCR polling failed.") from exc

        status = result_json.get("status")
        if status == "succeeded":
            return normalize_ocr_text(result_json)
        if status == "failed":
            reason = result_json.get("analyzeResult", {}).get("error", {}).get(
                "message", "Unknown reason"
            )
            raise AzureOcrFailedError(f"Azure OCR Failed: {reason}")
        if status not in {"notStarted", "running"}:
            raise AzureSubmissionError(f"Unknown Azure OCR status: {status}")

        attempts += 1
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(settings.azure_vision_poll_interval_seconds, remaining))

    raise AzureTimeoutError("OCR processing timeout (>60 seconds).")
