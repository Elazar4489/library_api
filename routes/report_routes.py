from fastapi import FastAPI, APIRouter, HTTPException
from routes.book_routes import bookdb
from routes.member_routes import memberdb
#from main import logger
import logging
logger = logging.getLogger()
router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def get_summary_report():
    logger.info("GET /reports/summary called")
    logger.info(f"Attempting a 'get summary report' request and successfully received")
    return {
        "total books": bookdb.count_total_books(),
        "available books": bookdb.count_available_books(),
        "currently books": bookdb.count_borrowed_books(),
        "active members": memberdb.count_active_members()
    }

@router.get("/books-by-genre")
def count_by_genre(genre):
    logger.info("GET /reports/books-by-genre called")
    try:
        logger.info(f"Attempting a 'count by genre', genre: {genre} request")
        by_genre = bookdb.count_by_genre(genre)
        logger.info(f"The request 'count by genre', genre: {genre} was successfully received")
        return by_genre
    except ValueError:
        logger.error(f"genre {genre} not found")
        raise HTTPException(status_code=400, detail=f"genre {genre} not found")

@router.get("/top-member")
def get_top_member():
    logger.info("GET /reports/top-members called")
    logger.info(f"Attempting a 'get top member' request and successfully received")
    return memberdb.get_top_member()
