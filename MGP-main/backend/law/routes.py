from fastapi import APIRouter
from .crud import fetch_all_laws

router = APIRouter()

@router.get("/laws")
def get_laws():
    return fetch_all_laws()