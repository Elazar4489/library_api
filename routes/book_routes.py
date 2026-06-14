from fastapi import APIRouter, HTTPException
from database import book_db
from routes.member_routes import memberdb

bookdb = book_db.BookDB()
member_class = memberdb
from database.book_db import TooMuchBooks
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

@router.put("/books/{id}/borrow/{member_id}")
def borrowed_book(book_id: int, member_id: int):
    member = member_class.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="member not exists.")
    elif member["is_active"] == False:
        raise HTTPException(status_code=400, detail="member is not active")
    try:
        borrow = bookdb.set_available(book_id, "borrowed", member_id)
        memberdb.increment_borrows(member_id)
        return borrow

    except KeyError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed")
    except NameError:
        raise HTTPException(status_code=404, detail="book not exists.")
    except TooMuchBooks:
        raise HTTPException(status_code=400, detail= "Member has reached maximum borrows")

@router.put("/books/{id}/return/{member_id}")
def return_book(book_id: int, member_id: int):
    member = member_class.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="member not exists.")
    try:
        return bookdb.set_available(book_id, "return", member_id)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is not borrowed")
    except NameError:
        raise HTTPException(status_code=404, detail="book not exists.")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed to someone else")


