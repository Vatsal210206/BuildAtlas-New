from io import BytesIO
from unittest.mock import Mock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

import hackathon
from backend.main import app
from backend.services import azure_ocr_service
from backend.services.bill_extraction_service import extract_bill_data


client = TestClient(app)


def image_bytes(image_format: str) -> bytes:
    image = Image.new("RGB", (40, 40), "white")
    output = BytesIO()
    image.save(output, format=image_format)
    return output.getvalue()


def mixed_bill_text() -> str:
    return "\n".join(
        [
            "ABC Cement Traders Ltd",
            "Invoice No: 12",
            "OPC Cement - 50 bags",
            "TMT Steel - 500 kg",
            "Red Bricks - 1000 nos",
            "River Sand - 2 ton",
            "Aggregate - 3 m3",
            f"Grand Total: {chr(0x20B9)}25,000.00",
        ]
    )


def test_extraction_matches_legacy_parser():
    text = mixed_bill_text()
    assert extract_bill_data(text) == hackathon.extract_bill_data(text)


def test_jpg_and_png_scan_responses():
    text = mixed_bill_text()
    with patch("backend.services.bill_scan_service.scan_image", return_value=text):
        jpg_response = client.post(
            "/api/bills/scan",
            files={"file": ("bill.jpg", image_bytes("JPEG"), "image/jpeg")},
        )
        png_response = client.post(
            "/api/bills/scan",
            files={"file": ("bill.png", image_bytes("PNG"), "image/png")},
        )

    assert jpg_response.status_code == 200
    assert png_response.status_code == 200
    assert jpg_response.json() == png_response.json()


def test_unsupported_files_are_rejected():
    response = client.post(
        "/api/bills/scan",
        files={"file": ("bill.pdf", b"pdf", "application/pdf")},
    )
    assert response.status_code == 415


def test_no_material_fallback_matches_legacy():
    text = f"Invoice text\nGrand Total: {chr(0x20B9)}100"
    with patch("backend.services.bill_scan_service.scan_image", return_value=text):
        response = client.post(
            "/api/bills/scan",
            files={"file": ("bill.jpg", image_bytes("JPEG"), "image/jpeg")},
        )

    assert response.status_code == 200
    assert response.json()["materials"] == hackathon.extract_bill_data(text)["materials"]


@pytest.mark.parametrize(
    ("exception", "status_code"),
    [
        (azure_ocr_service.AzureTimeoutError("timeout"), 504),
        (azure_ocr_service.AzureOcrFailedError("failed"), 502),
    ],
)
def test_azure_error_mapping(exception, status_code):
    with patch("backend.services.bill_scan_service.scan_image", side_effect=exception):
        response = client.post(
            "/api/bills/scan",
            files={"file": ("bill.jpg", image_bytes("JPEG"), "image/jpeg")},
        )
    assert response.status_code == status_code


def test_preprocessing_returns_png():
    processed = azure_ocr_service.preprocess_image(image_bytes("JPEG"))
    assert processed.startswith(b"\x89PNG")
    assert np.frombuffer(processed, dtype=np.uint8).size > 4


def test_azure_submit_poll_and_text_normalization():
    submit_response = Mock(status_code=202, headers={"Operation-Location": "https://azure.test/op"})
    running_response = Mock()
    running_response.json.return_value = {"status": "running"}
    succeeded_response = Mock()
    succeeded_response.json.return_value = {
        "status": "succeeded",
        "analyzeResult": {
            "readResults": [
                {"lines": [{"text": "Page one"}]},
                {"lines": [{"text": "Page two"}]},
            ]
        },
    }
    with patch.object(azure_ocr_service.settings, "azure_vision_endpoint", "https://azure.test"), patch.object(
        azure_ocr_service.settings, "azure_vision_key", "test-key"
    ), patch.object(azure_ocr_service.requests, "post", return_value=submit_response) as post, patch.object(
        azure_ocr_service.requests,
        "get",
        side_effect=[running_response, succeeded_response],
    ) as get, patch.object(azure_ocr_service.time, "sleep"):
        text = azure_ocr_service.scan_image(image_bytes("JPEG"))

    assert text == "Page one\nPage two"
    assert post.call_args.kwargs["headers"]["Content-Type"] == "application/octet-stream"
    assert get.call_count == 2
