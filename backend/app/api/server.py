from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core import tasks,config
from backend.app.api.routes import router as api_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await tasks.startup(app)
    yield
    await tasks.shutdown(app)


def get_application() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, 
                  version=config.VERSION,
                  lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    return app

app = get_application()
