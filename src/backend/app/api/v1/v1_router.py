from fastapi import APIRouter

from .au_router import au_router
from .la_router import la_router

v1_router = APIRouter(prefix="/v1/webhooks/clickfunnels")
v1_router.include_router(la_router)  # type: ignore
v1_router.include_router(au_router)  # type: ignore
