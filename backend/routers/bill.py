from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.schemas.bill import BillScanResponse
from backend.services.azure_ocr_service import BillScanError
from backend.services.bill_scan_service import (
    BillExtractionError,
    UnsupportedBillFileError,
    scan_bill,
)

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/scan", response_model=BillScanResponse)
async def scan_bill_route(file: UploadFile = File(...)) -> BillScanResponse:
    try:
        result = scan_bill(file.file, file.filename, file.content_type)
        return BillScanResponse(**result)
    except UnsupportedBillFileError as exc:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(exc)) from exc
    except BillExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    except BillScanError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
