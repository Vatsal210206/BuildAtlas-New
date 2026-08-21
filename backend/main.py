from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.routers.cost import router as cost_router
from backend.routers.bill import router as bill_router
from backend.routers.health import router as health_router

app = FastAPI(title="BuildAtlas API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(cost_router, prefix="/api")
app.include_router(bill_router, prefix="/api")
