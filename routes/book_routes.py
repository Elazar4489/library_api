from fastapi import APIRouter, HTTPException
from database import book_db
from routes.member_routes import memberdb
from database.book_db import TooMuchBooks, GenreError
#from main import logger
import logging
logger = logging.getLogger()
bookdb = book_db.BookDB()
member_class = memberdb
router = APIRouter()
@router.post("/books")
def create_book(title: str, author: str, genre: str):
    logger.info("POST /books called")
    try:
        logger.info("Attempting to create a new book")
        book_details=bookdb.create_book({"title": title, "author": author, "genre": genre})
        logger.info("New book added successfully")
        return book_details
    except GenreError:
        logger.error("the genre entered is not exists in the library!")
        raise HTTPException(status_code = 400, detail = "the genre you entered is not exists in the library!")

@router.get("/books")
def get_all_books():
    logger.info("GET /books called")
    logger.info("The request 'get all books' was successfully received")
    return bookdb.get_all_books()

@router.get("/books/{id}")
def get_book_by_id(book_id):
    logger.info("GET /books/{id} called")
    book = bookdb.get_book_by_id(book_id)
    logger.info(f"Attempting a 'get book by id', id: {book_id} request")
    if not book:
        logger.error(f"book {book_id} not exists")
        raise HTTPException(status_code= 404, detail= "book not exists.")
    logger.info(f"The request 'get book by id', id: {book_id} was successfully received")
    return book

@router.put("/books/{id}")
def update_book(book_id: int, title: str, author: str, genre: str):
    logger.info("PUT /books called")
    try:
        logger.info(f"Attempting a 'update book', id: {book_id} request")
        book_updated = bookdb.update_book(book_id, {"title": title, "author": author, "genre": genre})
        logger.info(f"The request 'update book', id: {book_id} was successfully received")
        return book_updated
    except GenreError:
        logger.error(f"the genre entered: {genre} is not exists in the library!")
        raise HTTPException(status_code = 400, detail = "the genre you entered is not exists in the library!")
    except IDNotFound:
        logger.error(f"book {book_id} not exists.")
        raise HTTPException(status_code= 404, detail= f"book {book_id} not exists.")

@router.put("/books/{id}/borrow/{member_id}")
def borrowed_book(book_id: int, member_id: int):
    logger.info("PUT /books/{id}/borrow/{member_id} called")
    logger.info(f"Attempting a 'borrowed book', id: {book_id} request")
    member = member_class.get_member_by_id(member_id)
    if not member:
        logger.error(f"member {member_id} not exists.")
        raise HTTPException(status_code=404, detail="member not exists.")
    elif member["is_active"] == False:
        logger.error(f"member {member_id} is not active")
        raise HTTPException(status_code=400, detail="member is not active")
    try:
        borrow = bookdb.set_available(book_id, "borrowed", member_id)
        memberdb.increment_borrows(member_id)
        logger.info(f"The request borrowed book, id: {book_id} to member, id: {member_id} was successfully received.")
        return borrow

    except KeyError:
        logger.error(f"the book: {book_id} is already borrowed")
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed")
    except IDNotFound:
        logger.error(f"book {book_id} not exists.")
        raise HTTPException(status_code=404, detail=f"book {book_id} not exists.")
    except TooMuchBooks:
        logger.error(f"Member id: {member_id} has reached maximum borrows")
        raise HTTPException(status_code=400, detail= f"Member id: {member_id} has reached maximum borrows")

@router.put("/books/{id}/return/{member_id}")
def return_book(book_id: int, member_id: int):
    logger.info("PUT /books/{id}/return/{member_id} called")
    member = member_class.get_member_by_id(member_id)
    logger.info(f"Attempting a 'return book', id: {book_id} request")
    if not member:
        logger.error(f"member {member_id} not exists.")
        raise HTTPException(status_code=404, detail=f"member {member_id} not exists.")
    try:
        return_b = bookdb.set_available(book_id, "return", member_id)
        logger.info(logger.info(f"The request return book, id: {book_id} from member, id: {member_id} was successfully received."))
        return return_b
    except KeyError:
        logger.error(f"the book: {book_id} is not borrowed")
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is not borrowed")
    except IDNotFound:
        logger.error(f"book {book_id} not exists.")
        raise HTTPException(status_code=404, detail=f"book {book_id} not exists.")
    except ValueError:
        logger.error(f"the book: {book_id} is already borrowed to someone else")
        raise HTTPException(status_code=400, detail=f"the book: {book_id} is already borrowed to someone else")


