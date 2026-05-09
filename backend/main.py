from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import capture, threats, alerts, stats, model
from database.mongodb import get_database

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(capture.router, prefix=f"{settings.API_V1_STR}/capture", tags=["Capture"])
app.include_router(threats.router, prefix=f"{settings.API_V1_STR}/threats", tags=["Threats"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["Alerts"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["Stats"])
app.include_router(model.router, prefix=f"{settings.API_V1_STR}/model", tags=["Model"])

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = await get_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    if hasattr(app, "mongodb_client"):
        app.mongodb_client.client.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Real-Time Cybersecurity Detection API"}
