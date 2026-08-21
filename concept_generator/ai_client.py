import os
import re
import time
from typing import Dict, Any, Callable, Optional

import requests

from .prompt_builder import build_prompt

try:
    from google.api_core import exceptions as google_exceptions
except ImportError:  # pragma: no cover - optional dependency
    google_exceptions = None


class ConceptGeneratorClient:
    def __init__(self, api_key: str = "", model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6IF04OENr4XZ9tZxIiiU1BouLnPqGpDGXPFYrExnNV3iw")
        # gemini-2.5-pro is the stronger alternative, but it is slower and more expensive.
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def _redact_sensitive_text(self, text: str) -> str:
        if not text:
            return text
        return re.sub(r"([?&](?:key|api[_-]?key)=)([^&#\s]+)", r"\1[REDACTED]", text, flags=re.IGNORECASE)

    def _get_error_status_code(self, exc: Exception) -> Optional[int]:
        response = getattr(exc, "response", None)
        if response is not None:
            status_code = getattr(response, "status_code", None)
            if isinstance(status_code, int):
                return status_code

        status_code = getattr(exc, "status_code", None)
        if isinstance(status_code, int):
            return status_code

        if hasattr(exc, "code") and isinstance(exc.code, int):
            return exc.code

        match = re.search(r"\b(4\d{2}|5\d{2})\b", str(exc))
        if match:
            return int(match.group(1))

        return None

    def _is_transient_error(self, exc: Exception) -> bool:
        if exc is None:
            return False

        status_code = self._get_error_status_code(exc)
        if status_code in {429, 500, 502, 503, 504}:
            return True

        if isinstance(exc, requests.exceptions.Timeout | requests.exceptions.ConnectionError):
            return True

        if isinstance(exc, requests.exceptions.RequestException):
            if status_code in {408}:
                return True

        if google_exceptions is not None:
            transient_google_types = []
            for class_name in [
                "ServiceUnavailable",
                "TooManyRequests",
                "DeadlineExceeded",
                "InternalServerError",
                "ResourceExhausted",
                "Aborted",
                "Unavailable",
            ]:
                candidate = getattr(google_exceptions, class_name, None)
                if candidate is not None:
                    transient_google_types.append(candidate)
            if transient_google_types and isinstance(exc, tuple(transient_google_types)):
                return True

        message = str(exc).lower()
        return any(token in message for token in ["temporarily unavailable", "rate limit", "too many requests", "service unavailable", "deadline exceeded", "retry later", "try again later"])

    def _extract_text(self, response_payload: Any) -> str:
        try:
            if hasattr(response_payload, "text") and response_payload.text:
                return str(response_payload.text).strip()

            if hasattr(response_payload, "candidates") and response_payload.candidates:
                candidate = response_payload.candidates[0]
                parts = getattr(candidate, "content", None)
                if parts is not None and hasattr(parts, "parts"):
                    text_blocks = []
                    for part in parts.parts:
                        if hasattr(part, "text") and part.text:
                            text_blocks.append(str(part.text))
                    text = "\n".join(text_blocks).strip()
                    if text:
                        return text

            if isinstance(response_payload, dict):
                if response_payload.get("candidates"):
                    candidate = response_payload["candidates"][0]
                    content = candidate.get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        return "\n".join(str(part.get("text", "")) for part in parts if part.get("text")).strip()
                return str(response_payload.get("text", "")).strip()

            return str(response_payload).strip()
        except Exception:
            return ""

    def generate_concept(
        self,
        project_type: str,
        structured_requirements: Dict[str, Any],
        lifestyle_context: str,
        plot_info: Dict[str, Any],
        variant_hint: str = "",
        status_callback: Optional[Callable[[str], None]] = None,
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("Gemini API key is not configured. Set the GEMINI_API_KEY environment variable before generating a concept.")

        prompt = build_prompt(project_type, structured_requirements, lifestyle_context, plot_info, variant_hint)
        print(f"[Concept Prompt Debug] {prompt}")

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "max_output_tokens": 4096,
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "concept_summary": {"type": "STRING"},
                        "zoning_logic": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "space_allocation": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "zone_name": {"type": "STRING"},
                                    "area_sqft": {"type": "NUMBER"},
                                    "percent": {"type": "NUMBER"}
                                },
                                "required": ["zone_name", "area_sqft", "percent"]
                            }
                        },
                        "adjacency_rationale": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "future_expansion": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "disclaimer": {"type": "STRING"},
                        "diagram": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "label": {"type": "STRING"},
                                    "area": {"type": "NUMBER"},
                                    "adjacency": {"type": "ARRAY", "items": {"type": "STRING"}}
                                },
                                "required": ["label", "area", "adjacency"]
                            }
                        }
                    },
                    "required": [
                        "concept_summary",
                        "zoning_logic",
                        "space_allocation",
                        "adjacency_rationale",
                        "future_expansion",
                        "disclaimer",
                        "diagram"
                    ]
                },
            },
        }

        max_retries = 3
        last_error: Optional[Exception] = None

        for attempt in range(1, max_retries + 2):
            try:
                url = f"{self.endpoint}?key={self.api_key}"
                response = requests.post(url, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
                break
            except requests.exceptions.RequestException as exc:
                last_error = exc
                if attempt <= max_retries and self._is_transient_error(exc):
                    retry_delay = 2 ** attempt
                    if status_callback is not None:
                        status_callback(f"Gemini is temporarily busy, retrying... (attempt {attempt + 1} of {max_retries + 1})")
                    time.sleep(retry_delay)
                    continue
                raise RuntimeError(self._format_error_message(exc, transient=False)) from exc
            except Exception as exc:  # pragma: no cover - defensive fallback
                last_error = exc
                raise RuntimeError(self._format_error_message(exc, transient=False)) from exc
        else:
            if last_error is not None:
                raise RuntimeError(self._format_error_message(last_error, transient=True)) from last_error
            raise RuntimeError("Gemini request failed while generating the concept.")

        candidates = data.get("candidates", []) if isinstance(data, dict) else []
        if candidates:
            finish_reason = candidates[0].get("finishReason") if isinstance(candidates[0], dict) else None
            if finish_reason == "MAX_TOKENS":
                raise RuntimeError("Gemini response was truncated (hit the max_output_tokens limit). Increase max_output_tokens and retry.")

        text = self._extract_text(data)
        print(f"[Raw Gemini Response - length {len(text)} chars]\n{text}\n[End Raw Response]")
        if not text:
            raise RuntimeError("Gemini returned a malformed response without usable text content.")

        return {
            "raw_prompt": prompt,
            "raw_text": text,
            "response_payload": data,
        }

    def _format_error_message(self, exc: Exception, *, transient: bool) -> str:
        redacted_message = self._redact_sensitive_text(str(exc))
        if transient:
            return (
                f"Gemini request failed while generating the concept: {redacted_message}. "
                "Gemini's servers are temporarily unavailable. Please wait a moment and click Generate Concept again."
            )
        return f"Gemini request failed while generating the concept: {redacted_message}"
