from fastapi import FastAPI, APIRouter, HTTPException
from routes.book_routes import bookdb
from routes.member_routes import memberdb


router = APIRouter()

@router.get("/reports/summary")
def get_summary_report():
    return {
        "total books": bookdb.count_total_books(),
        "available books": bookdb.count_available_books(),
        "currently books": bookdb.count_borrowed_books(),
        "active members": memberdb.count_active_members()
    }

@router.get("/reports/books-by-genre")
def count_by_genre(genre):
    try:
        by_genre = bookdb.count_by_genre(genre)
        return by_genre
    except ValueError:
        raise HTTPException(status_code=400, detail="genre not found")

@router.get("/reports/top-member")
def get_top_member():
    return memberdb.get_top_member()
