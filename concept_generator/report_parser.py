# report_parser.py — full replacement

import json
import re
from typing import Dict, Any, List

DEFAULT_DISCLAIMER = "Conceptual visualization only — consult a licensed architect before construction."

_SCHEMA_KEYS = {"concept_summary", "zoning_logic", "space_allocation", "adjacency_rationale", "future_expansion"}


def _clean_raw_text(raw_text: str) -> str:
    if not isinstance(raw_text, str):
        return ""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:html|json|markdown|md)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _is_schema_dict(d: Any) -> bool:
    return isinstance(d, dict) and _SCHEMA_KEYS.issubset(d.keys())


def _parse_sections(raw_text: str) -> Dict[str, Any]:
    heading_pattern = re.compile(
        r"(?im)^\s*(?:#+\s*)?(Concept Summary|Zoning Logic|Space Allocation|Adjacency Rationale|Future Expansion Ideas)\s*:?\s*$"
    )
    matches = list(heading_pattern.finditer(raw_text))
    if not matches:
        return {}
    sections: Dict[str, Any] = {}
    for idx, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_text)
        sections[heading] = raw_text[start:end].strip()
    return sections


def _parse_space_lines(content: str) -> List[Dict[str, Any]]:
    allocation = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.search(r"(?:[-*]\s*)?(.*?)(?:\s*[-–—]\s*|\s*:\s*)(\d+(?:\.\d+)?)\s*(?:sq\s*ft|sqft|ft²|ft2|sq ft)?\s*(?:\(|\[)?\s*(\d+(?:\.\d+)?)\s*%?", line, re.IGNORECASE)
        if not match:
            continue
        zone_name = match.group(1).strip().strip("-")
        allocation.append({
            "zone_name": zone_name,
            "area_sqft": int(round(float(match.group(2)))),
            "percent": round(float(match.group(3)), 1),
        })
    return allocation


def _normalize_space_allocation(space_allocation: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in space_allocation or []:
        zone_name = item.get("zone_name") or item.get("space") or item.get("label") or "Zone"
        area_sqft = item.get("area_sqft") or item.get("area") or 0
        percent = item.get("percent") or item.get("pct") or 0
        normalized.append({"zone_name": zone_name, "area_sqft": int(area_sqft), "percent": round(float(percent), 1)})
    return normalized


def _diagram_from_allocation(space_allocation: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "label": item.get("zone_name") or item.get("space") or "Zone",
            "area": int(item.get("area_sqft") or item.get("area") or 0),
            "adjacency": [],
        }
        for item in (space_allocation or [])
    ]


def _normalize_schema_dict(parsed: Dict[str, Any]) -> Dict[str, Any]:
    space_allocation = _normalize_space_allocation(parsed.get("space_allocation", []))
    diagram = parsed.get("diagram") or _diagram_from_allocation(space_allocation)
    return {
        "concept_summary": parsed.get("concept_summary") or "A conceptual layout is being prepared for review.",
        "zoning_logic": parsed.get("zoning_logic") or [],
        "space_allocation": space_allocation,
        "adjacency_rationale": parsed.get("adjacency_rationale") or [],
        "future_expansion": parsed.get("future_expansion") or [],
        "diagram": diagram,
        "disclaimer": parsed.get("disclaimer") or DEFAULT_DISCLAIMER,
    }


def _normalize_text_sections(parsed: Dict[str, Any]) -> Dict[str, Any]:
    # Legacy fallback only: markdown-style "Heading\ncontent" parsing, used
    # when Gemini returns free-form text instead of matching the schema.
    concept_summary = parsed.get("Concept Summary", "")
    zoning_logic = [l.strip().lstrip("-*") for l in parsed.get("Zoning Logic", "").splitlines() if l.strip()]
    space_content = parsed.get("Space Allocation", "")
    space_allocation = _parse_space_lines(space_content) or _normalize_space_allocation(parsed.get("space_allocation", []))
    adjacency_rationale = [l.strip().lstrip("-*") for l in parsed.get("Adjacency Rationale", "").splitlines() if l.strip()]
    future_expansion = [l.strip().lstrip("-*") for l in parsed.get("Future Expansion Ideas", "").splitlines() if l.strip()]
    return {
        "concept_summary": concept_summary,
        "zoning_logic": zoning_logic,
        "space_allocation": space_allocation,
        "adjacency_rationale": adjacency_rationale,
        "future_expansion": future_expansion,
        "diagram": _diagram_from_allocation(space_allocation),
        "disclaimer": parsed.get("disclaimer", DEFAULT_DISCLAIMER),
    }


def _empty_report() -> Dict[str, Any]:
    return {
        "concept_summary": "A conceptual layout is being prepared for review.",
        "zoning_logic": [], "space_allocation": [], "adjacency_rationale": [],
        "future_expansion": [], "diagram": [], "disclaimer": DEFAULT_DISCLAIMER,
    }


def normalize_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        return _empty_report()
    if isinstance(payload, str):
        payload = {"raw_text": payload}
    if isinstance(payload, dict):
        if _is_schema_dict(payload):
            return _normalize_schema_dict(payload)

        raw_text = _clean_raw_text(payload.get("raw_text", payload.get("text", "")))
        if raw_text:
            parsed = {}
            try:
                parsed_json = json.loads(raw_text)
                if isinstance(parsed_json, dict):
                    parsed = parsed_json
            except Exception as exc:
                try:
                    parsed_json = json.loads(raw_text.replace("\n", "\\n"))
                    if isinstance(parsed_json, dict):
                        parsed = parsed_json
                except Exception:
                    print(f"normalize_report JSON parse failure. raw_text=\n{raw_text}")
                    raise ValueError(f"Gemini JSON parsing failed: {exc}. raw_text was: {raw_text}") from exc

            if _is_schema_dict(parsed):
                return _normalize_schema_dict(parsed)
            return _normalize_text_sections(parsed)
    return _empty_report()