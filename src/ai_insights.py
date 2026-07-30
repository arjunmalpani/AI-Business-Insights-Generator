from __future__ import annotations

import json
import logging
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai

from prompts import BUSINESS_PROMPT

load_dotenv()

LOGGER = logging.getLogger(__name__)


class AIInsightsError(RuntimeError):
    """Raised when the insight service cannot produce a reportable payload."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class AIInsights:
    """Thin wrapper around the Gemini client for generating business insight payloads."""

    DEFAULT_MODEL = "gemini-3.5-flash-lite"
    DEFAULT_REPORT_PATH = Path("reports/report.md")
    MAX_PROMPT_LENGTH = 200_000

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model_name: str | None = None,
        report_path: str | Path | None = None,
    ) -> None:
        resolved_api_key = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
        if not resolved_api_key:
            raise AIInsightsError("Missing GEMINI_API_KEY configuration for insight generation.")

        self.client = genai.Client(api_key=resolved_api_key)
        self.model_name = model_name or self.DEFAULT_MODEL
        self.report_path = Path(report_path or self.DEFAULT_REPORT_PATH)

    def generate_insights(self, kpis: Any, *, request_id: str | None = None) -> dict[str, Any]:
        """Generate structured business insights for the supplied KPI payload.

        The method accepts either a pre-serialized KPI payload or a mapping so the
        caller can pass either a plain dictionary or the JSON string emitted by the
        analytics pipeline.
        """

        normalized_kpis = self._normalize_kpi_payload(kpis)
        if not normalized_kpis:
            LOGGER.warning(
                "No KPI payload supplied for insight generation",
                extra={"request_id": request_id},
            )
            return self._build_error_response("No KPI payload was provided for insight generation.")

        prompt = BUSINESS_PROMPT.format(kpis=normalized_kpis)
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            raise AIInsightsError(
                "Prompt exceeds the maximum supported size for the selected model.",
                details={"prompt_length": len(prompt)},
            )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            raw_text = getattr(response, "text", None)
        except Exception as exc:  # pragma: no cover - exercised in production when the API is unavailable
            LOGGER.exception(
                "AI insight generation failed",
                extra={"request_id": request_id, "model_name": self.model_name},
            )
            return self._build_error_response(
                "Unable to generate business insights at the moment.",
                details={"error_type": type(exc).__name__},
            )

        if not isinstance(raw_text, str) or not raw_text.strip():
            LOGGER.error(
                "Model returned an empty payload",
                extra={"request_id": request_id, "model_name": self.model_name},
            )
            return self._build_error_response("The model returned an empty response.")

        # The model occasionally wraps JSON in markdown fences, so we normalize that before parsing.
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.strip("`").strip()

        try:
            parsed_payload = json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            LOGGER.warning(
                "Model returned malformed JSON",
                extra={
                    "request_id": request_id,
                    "model_name": self.model_name,
                    "payload_length": len(cleaned_text),
                },
            )
            return self._build_error_response(
                "The model returned malformed JSON.",
                details={"decode_error": str(exc)},
            )

        if not isinstance(parsed_payload, dict):
            LOGGER.warning(
                "Model returned an unexpected payload shape",
                extra={"request_id": request_id, "model_name": self.model_name},
            )
            return self._build_error_response(
                "The model returned an unexpected payload shape.",
                details={"payload_type": type(parsed_payload).__name__},
            )

        LOGGER.info(
            "AI insights generated successfully",
            extra={
                "request_id": request_id,
                "model_name": self.model_name,
                "section_count": len(parsed_payload),
            },
        )
        return parsed_payload

    def save_report(self, insights: Any, *, report_path: str | Path | None = None) -> Path:
        """Persist the generated insights to disk as plain text for downstream reporting."""

        if not isinstance(insights, (str, dict)):
            raise AIInsightsError(
                "Insights must be a string or dictionary payload before they can be saved.",
                details={"received_type": type(insights).__name__},
            )

        target_path = Path(report_path or self.report_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        content = json.dumps(insights, indent=2, sort_keys=True) if isinstance(insights, dict) else insights
        target_path.write_text(content, encoding="utf-8")

        LOGGER.info("Insights report written", extra={"report_path": str(target_path)})
        return target_path

    def _normalize_kpi_payload(self, kpis: Any) -> str:
        if isinstance(kpis, str):
            return kpis.strip() or "{}"
        if isinstance(kpis, Mapping):
            return json.dumps(dict(kpis), indent=4, default=str)
        if kpis is None:
            return "{}"
        return json.dumps(kpis, indent=4, default=str)

    def _build_error_response(self, message: str, *, details: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "executive_summary": [message],
            "error": {
                "message": message,
                "details": details or {},
            },
        }
