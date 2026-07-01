from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api import auth, devices
app = FastAPI(
    title=settings.APP_NAME,
    description="Network monitoring and infrastructure management platform",
    version="0.1.0",
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(devices.router)



# React dev server
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.ENVIRONMENT}