from unittest.mock import patch

import pytest
import requests

import concept_generator.ai_client as ai_client


class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"{self.status_code} error for url: https://example.com/generate?key=super-secret-key"
            )

    def json(self):
        return self._payload


def test_generate_concept_retries_transient_errors_and_succeeds():
    client = ai_client.ConceptGeneratorClient(api_key="test-key")
    transient_response = DummyResponse(503)
    success_payload = {
        "candidates": [
            {"content": {"parts": [{"text": '{"concept_summary":"ok"}'}]}}
        ]
    }
    success_response = DummyResponse(200, success_payload)

    with patch.object(ai_client, "build_prompt", return_value="prompt"), patch.object(
        ai_client.requests,
        "post",
        side_effect=[transient_response, success_response],
    ) as mock_post, patch.object(ai_client.time, "sleep", return_value=None) as mock_sleep:
        status_updates = []
        result = client.generate_concept(
            "house",
            {},
            "lifestyle",
            {"plot_width": 20, "plot_length": 30},
            status_callback=status_updates.append,
        )

    assert mock_post.call_count == 2
    assert status_updates[-1] == "Gemini is temporarily busy, retrying... (attempt 2 of 4)"
    assert mock_sleep.call_count == 1
    assert mock_sleep.call_args_list[0].args[0] == 2
    assert result["raw_text"] == '{"concept_summary":"ok"}'


def test_generate_concept_does_not_retry_permanent_errors():
    client = ai_client.ConceptGeneratorClient(api_key="test-key")
    response = DummyResponse(401)

    with patch.object(ai_client, "build_prompt", return_value="prompt"), patch.object(
        ai_client.requests,
        "post",
        return_value=response,
    ) as mock_post:
        with pytest.raises(RuntimeError) as exc_info:
            client.generate_concept(
                "house",
                {},
                "lifestyle",
                {"plot_width": 20, "plot_length": 30},
            )

    assert mock_post.call_count == 1
    assert "super-secret-key" not in str(exc_info.value)
    assert "temporarily unavailable" not in str(exc_info.value)
