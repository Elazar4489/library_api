from fastapi import FastAPI, APIRouter, HTTPException
from database import book_db
bookdb = book_db.BookDB()

router = APIRouter()
@router.post("/books")
def create_book(title: str, author: str, genre: str):
    try:
        book_details=bookdb.create_book({"title": title, "author": author, "genre": genre})
        return book_details
    except KeyError:
        raise HTTPException(status_code = 400, detail= "you entered key error in data.")
    except ValueError:
        raise HTTPException(status_code = 400, detail = "the genre you entered is not exists in the library!")

@router.get("/books")
def get_all_books():
    return bookdb.get_all_books()

@router.get("/books/{id}")
def get_book_by_id(book_id):
    book = bookdb.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code= 404, detail= "book not exists.")
    return book

@router.put("/books/{id}")
def update_book(book_id: int, title: str, author: str, genre: str):
    try:
        book_updated = bookdb.update_book(book_id, {"title": title, "author": author, "genre": genre})
        return book_updated
    except KeyError:
        raise HTTPException(status_code = 400, detail= "you entered key error in data.")
    except ValueError:
        raise HTTPException(status_code = 400, detail = "the genre you entered is not exists in the library!")
    except NameError:
        raise HTTPException(status_code= 404, detail= "book not exists.")

@router.put("/books/{id}/borrowed/{member_id}")
def borrowed_book(book_id: int, member_id: int):
    try:
        return bookdb.set_available(book_id, "borrowed", member_id)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed")
    except NameError:
        raise HTTPException(status_code=404, detail="book not exists.")

@router.put("/books/{id}/return/{member_id}")
def return_book(book_id: int, member_id: int):
    try:
        return bookdb.set_available(book_id, "return", member_id)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is not borrowed")
    except NameError:
        raise HTTPException(status_code=404, detail="book not exists.")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed to someone else")
 #TODO להוסיף שגיאות בחבר בשני הפונקציות האחרונות



