import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from config import settings
from database.db import Base, engine
from models.generation import GenerationData
from models.pricing import PricingData
from models.renewable import RenewableData
from api.routes import router
from services.scheduler_service import start_daily_update
from utils.logger import setup_logger

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행할 작업"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

    scheduler = BackgroundScheduler()
    scheduler.add_job(start_daily_update, "cron", hour=0, minute=0)
    scheduler.start()
    logger.info("Scheduler started - Daily update at 00:00 UTC")

    yield

    scheduler.shutdown()
    logger.info("Scheduler shutdown")

app = FastAPI(
    title="US Power Grid Dashboard API",
    description="미국 전력망 모니터링 API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "US Power Grid Dashboard API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
