from fastapi import FastAPI, APIRouter



router = APIRouter()
@router.get("/test")
def testt():
    return "hello"