from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from backend.schemas.cost import CostPredictionRequest, CostPredictionResponse


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "cost_model.pkl"
DEFAULT_COLUMNS_PATH = PROJECT_ROOT / "model_columns.pkl"


class CostArtifactError(RuntimeError):
    """Raised when the existing cost model artifacts cannot be loaded."""


class CostPredictionError(RuntimeError):
    """Raised when the existing cost model cannot produce a prediction."""


@lru_cache(maxsize=1)
def _load_artifacts() -> tuple[object, object]:
    if not DEFAULT_MODEL_PATH.is_file():
        raise CostArtifactError(f"Cost model artifact not found: {DEFAULT_MODEL_PATH}")
    if not DEFAULT_COLUMNS_PATH.is_file():
        raise CostArtifactError(f"Cost model columns artifact not found: {DEFAULT_COLUMNS_PATH}")

    try:
        model = joblib.load(DEFAULT_MODEL_PATH)
        columns = joblib.load(DEFAULT_COLUMNS_PATH)
    except Exception as exc:
        raise CostArtifactError("Unable to load cost model artifacts") from exc

    return model, columns


def predict_cost(request: CostPredictionRequest) -> CostPredictionResponse:
    model, _columns = _load_artifacts()

    input_data = pd.DataFrame(
        {
            "size": [request.size],
            "floors": [request.floors],
            "project_type": [request.project_type],
            "city": [request.city],
        }
    )

    # Keep this feature engineering identical to hackathon.py.
    input_data["size_per_floor"] = input_data["size"] / input_data["floors"]
    input_data["total_area"] = input_data["size"] * input_data["floors"]
    input_data["log_size"] = np.log1p(input_data["size"])

    try:
        base_cost = float(model.predict(input_data)[0])
    except Exception as exc:
        raise CostPredictionError("Cost model prediction failed") from exc

    total_cost = base_cost * 1.1
    return CostPredictionResponse(
        size=request.size,
        floors=request.floors,
        project_type=request.project_type,
        city=request.city,
        base_cost=base_cost,
        total_cost=total_cost,
        total_cost_crore=total_cost / 10_000_000,
    )
