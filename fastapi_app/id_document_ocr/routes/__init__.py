
from fastapi import APIRouter
from .document_ocr_route import router

api_router = APIRouter()
api_router.include_router(router)
