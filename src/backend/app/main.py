from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import api_router
from .config import get_config
from .utils import TraceIDMiddleware, lifespan, setup_error_handling

config = get_config()

app = FastAPI(
    lifespan=lifespan,
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    docs_url="/docs" if config.ENABLE_API_DOCS else None,
    redoc_url="/redoc" if config.ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if config.ENABLE_API_DOCS else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(TraceIDMiddleware)

app.include_router(api_router)

setup_error_handling(app=app)


@app.get("/")
async def healthcheck():
    return {"ok": True, "message": "it works!! :tada:"}
