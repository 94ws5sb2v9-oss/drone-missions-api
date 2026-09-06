from fastapi import FastAPI

from app.api.routes import router
from app.database.db import engine
from app.models.mission import Base

from contextlib import asynccontextmanager

from app.core.config import APP_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    lifespan=lifespan,
)


app.include_router(router)


@app.get("/")
def root():
    return {"message": "Drone Missions API"}
