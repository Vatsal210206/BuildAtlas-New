from fastapi import APIRouter, HTTPException, status

from backend.schemas.cost import CostPredictionRequest, CostPredictionResponse
from backend.services.cost_service import CostArtifactError, CostPredictionError, predict_cost

router = APIRouter(prefix="/cost", tags=["cost"])


@router.post(
    "/predict",
    response_model=CostPredictionResponse,
    status_code=status.HTTP_200_OK,
)
def predict_cost_route(request: CostPredictionRequest) -> CostPredictionResponse:
    try:
        return predict_cost(request)
    except CostArtifactError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except CostPredictionError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
