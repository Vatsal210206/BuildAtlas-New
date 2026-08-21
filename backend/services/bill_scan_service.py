from typing import BinaryIO

from backend.services.azure_ocr_service import scan_image
from backend.services.bill_extraction_service import extract_bill_data


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
SUPPORTED_CONTENT_TYPES = {"image/jpeg", "image/png"}


class UnsupportedBillFileError(ValueError):
    pass


class BillExtractionError(RuntimeError):
    pass


def validate_bill_file(filename: str | None, content_type: str | None) -> None:
    extension = ""
    if filename:
        extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in SUPPORTED_EXTENSIONS or content_type not in SUPPORTED_CONTENT_TYPES:
        raise UnsupportedBillFileError(
            "Unsupported bill file. Upload a JPG, JPEG, or PNG image."
        )


def scan_bill(file: BinaryIO, filename: str | None, content_type: str | None) -> dict:
    validate_bill_file(filename, content_type)
    image_bytes = file.read()
    if not image_bytes:
        raise UnsupportedBillFileError("The uploaded bill file is empty.")

    raw_text = scan_image(image_bytes)
    try:
        extracted = extract_bill_data(raw_text)
    except Exception as exc:
        raise BillExtractionError("OCR succeeded but bill data extraction failed.") from exc

    return {**extracted, "raw_text": raw_text, "ocr_success": True}
