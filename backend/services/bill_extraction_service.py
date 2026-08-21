from datetime import datetime
import re
from typing import Any


def extract_bill_data(ocr_text: Any) -> dict[str, Any]:
    if not ocr_text or not isinstance(ocr_text, str):
        return {
            "supplier": "Unknown",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": 0,
            "materials": [],
        }

    materials = []
    total_amount = 0
    supplier = "Unknown Supplier"
    lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]

    for line in lines[:10]:
        if re.search(
            r"(cement|steel|builders|construction|ltd|pvt|supplies?|traders?|pvt\.?|co\.?)",
            line,
            re.IGNORECASE,
        ):
            supplier = line[:50]
            break

    for line in lines:
        cement_match = re.search(
            r"(opc\s*cement|ppc\s*cement|portland\s*cement|cement)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(bag|bags|kg|ton|tons|units?)",
            line,
            re.IGNORECASE,
        )
        if cement_match:
            name = (
                "OPC Cement"
                if "opc" in line.lower()
                else "PPC Cement"
                if "ppc" in line.lower()
                else "Cement"
            )
            materials.append(
                {
                    "name": name,
                    "quantity": float(cement_match.group(2)),
                    "unit": cement_match.group(3),
                    "rate": 0,
                    "total": 0,
                }
            )

        steel_match = re.search(
            r"(tmt\s*steel|steel\s*bar|steel\s*rod|tmt|rebar)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(kg|kg\s*per|ton|tons|units?|bars?|pieces?)",
            line,
            re.IGNORECASE,
        )
        if steel_match:
            materials.append(
                {
                    "name": "TMT Steel",
                    "quantity": float(steel_match.group(2)),
                    "unit": steel_match.group(3),
                    "rate": 0,
                    "total": 0,
                }
            )

        brick_match = re.search(
            r"(brick|bricks|clay\s*brick|red\s*brick)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(nos?|pieces?|units?|thousand)",
            line,
            re.IGNORECASE,
        )
        if brick_match:
            materials.append(
                {
                    "name": "Bricks",
                    "quantity": float(brick_match.group(2)),
                    "unit": brick_match.group(3),
                    "rate": 0,
                    "total": 0,
                }
            )

        sand_match = re.search(
            r"(sand|river\s*sand|concrete\s*sand)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(ton|tons|cubic|m3|m³|cum|units?|bags?)",
            line,
            re.IGNORECASE,
        )
        if sand_match:
            materials.append(
                {
                    "name": "Sand",
                    "quantity": float(sand_match.group(2)),
                    "unit": sand_match.group(3),
                    "rate": 0,
                    "total": 0,
                }
            )

        aggregate_match = re.search(
            r"(aggregate|gravel|crusher\s*sand|coarse\s*aggregate)\s*[–\-x]?\s*(\d+(?:\.\d+)?)\s*(ton|tons|cubic|m3|m³|cum|units?)",
            line,
            re.IGNORECASE,
        )
        if aggregate_match:
            materials.append(
                {
                    "name": "Aggregate",
                    "quantity": float(aggregate_match.group(2)),
                    "unit": aggregate_match.group(3),
                    "rate": 0,
                    "total": 0,
                }
            )

        total_match = re.search(
            r"(?:total|amount|grand\s*total|bill\s*amount)[\s:]*₹?[\s]?([0-9,]+(?:\.[0-9]{2})?)",
            line,
            re.IGNORECASE,
        )
        if total_match:
            try:
                total_amount = float(total_match.group(1).replace(",", ""))
            except ValueError:
                pass

    if not materials:
        materials = [
            {
                "name": "Materials Detected",
                "quantity": len([line for line in lines if len(line) > 5]),
                "unit": "lines",
                "rate": 0,
                "total": total_amount,
            }
        ]

    return {
        "supplier": supplier,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": int(total_amount),
        "materials": materials,
    }
