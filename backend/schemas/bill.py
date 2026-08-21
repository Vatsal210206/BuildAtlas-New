from pydantic import BaseModel


class MaterialResult(BaseModel):
    name: str
    quantity: float
    unit: str
    rate: float
    total: float


class BillScanResponse(BaseModel):
    supplier: str
    date: str
    total: int
    materials: list[MaterialResult]
    raw_text: str
    ocr_success: bool
