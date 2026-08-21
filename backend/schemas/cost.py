from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProjectType = Literal["Residential", "Commercial", "Industrial"]
City = Literal["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune"]


class CostPredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    size: int = Field(default=1000, ge=1, description="Area in square metres")
    floors: int = Field(default=2, ge=1, description="Number of floors")
    project_type: ProjectType = "Residential"
    city: City = "Delhi"


class CostPredictionResponse(BaseModel):
    size: int
    floors: int
    project_type: ProjectType
    city: City
    base_cost: float
    total_cost: float
    currency: str = "INR"
    total_cost_crore: float
