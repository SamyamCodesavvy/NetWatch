from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging, os

from app.config import get_settings
from app.scheduler.jobs import start_scheduler, scheduler
from app.api import auth, devices, monitoring

settings = get_settings()
os.makedirs("logs", exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("logs/application.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    start_scheduler()
    yield
    scheduler.shutdown()
    logger.info("Shutting down...")

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION,
              description="Network Monitoring & Infrastructure Management Platform",
              lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(monitoring.router)

# To allow the React dev server(localhost:5173) to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:80", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}