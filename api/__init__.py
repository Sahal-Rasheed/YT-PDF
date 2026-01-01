from fastapi import APIRouter

from api.convert import convert_router

api_router = APIRouter()


api_router.include_router(convert_router, prefix="/convert", tags=["convert"])
