# Library API

___

## Project Description

This project is a library management system administrator.
The project raises a server with a certain number of nodes whose main function is to manage the library with a CRUD model.
The project's construction and operation are based on OOP, servers, and databases.
The main goals of the project are to allow the library to be managed properly, both in terms of book management and member management, in a way that all data is saved and synchronized.
The project is intended primarily for library managers and the like.

## Technologies Used

- Python
- pycharm
- FastAPI
- APIRouter
- pydantic
- MySQL
- Docker
- OOP

## Folder Structure

library-api/

├── main.py

├── database/

│   ├── db_connection.py

│   ├── book_db.py

│   └── member_db.py

├── routes/

│   ├── book_routes.py

│   ├── member_routes.py

│   └── report_routes.py

├── logs/

│   └── app.log

├── README.md

├── requirements.txt

└── .gitignore

## Docker Setup

```bash
docker run --name mysql_libraey 
-e MYSQL_ROOT_PASSWORD=root
-e MYSQL_DATABASE=library_db 
-p 3306:3306 -d mysql:8
```

## Database Information

`library_db`

## Database Tables

### Table: `books`

| Column Name           | Data Type   | Constraints  | Description                           |
|-----------------------|-------------|--------------|---------------------------------------|
| id                    | INT         | PRIMARY KEY  | master key                            |
| title                 | VARCHAR(50) | NOT NULL     | book title                            |
| author                | VARCHAR(50) | NOT NULL     | author's name                         |
| genre                 | ENUM        | NOT NULL     | allowed genre values                  |
| is_available          | BOOLEAN     | NOT NULL     | is the book available for loan?       |
| borrowed_by_member_id | INT         |              | the id of the member holding the book |

### Table: `members`

| Column Name    | Data Type   | Constraints | Description                    |
|----------------|-------------|-------------|--------------------------------|
| id             | INT         | PRIMARY KEY | master key                     |
| name           | VARCHAR(50) | NOT NULL    | member's name                  |
| email          | VARCHAR(50) | NOT NULL    | member's email address         |
| is_active      | BOOLEAN     | NOT NULL    | is the member active?          |
| total_borrowed | INT         | NOT NULL    | count total number of borrowed |


## System Rules

1. Create a book: User submits - genre/author/title. system adds: `is_available=True, borrowed_by=NULL`.
2. Genre: Must be - Fiction / Non-Fiction / Science / History / Other any other value return an ERROR (make sure to check both the addition (POST) and the update (PUT)).
3. Create a member: User submits - name/email. system adds: `is_active+True, total_borrows=0`.
4. Email: Must be unique — if it already exists returns an error
5. Inactive member: if `is_active = False` he can't borrow book.
6. Book unavailable: cannot borrow a book that has already been borrowed.
7. Maximum books: a member cannot hold more than 3 books at a time.
8. Returning a book: a book can only be returned if it is owned by the same member who owns it.

---

## API Endpoints

### Books Endpoints

| Method | Endpoint                           | Description    | Request Body                                                                 | Response                           |
|--------|------------------------------------|----------------|------------------------------------------------------------------------------|------------------------------------|
| POST   | "/books"                           | create a book  | `{"title": "...", "author": "...", "genre": "..."}`                          | Returns the created book with ID   |
| GET    | "/books"                           | get all books  | None                                                                         | Returns list of all dicts of books |
| GET    | "/books/{id}"                      | get book by id | `{"book_id": ...}`                                                           | Returns dict of one book by id     |
| PUT    | "/books/{id}"                      | update book    | `{"book_id": ...,"data": {"title": "...", "author": "...", "genre": "..."}}` | Returns the updated book           |
| PUT    | "/books/{id}/borrowed/{member_id}" | borrowed book  | `{"book_id": ..., "member_id"}`                                              | Returns the updated book           |
| PUT    | "/books/{id}/return/{member_id}"   | return book    | `{"book_id": ..., "member_id"}`                                              | Returns the updated book           |


---

### Members Endpoints

| Method | Endpoint                  | Description       | Request Body                                                   | Response                             |
|--------|---------------------------|-------------------|----------------------------------------------------------------|--------------------------------------|
| POST   | "/member"                 | create member     | `{"name": "...", "email": "..."}`                              | Returns the created member with ID   |
| GET    | "/member"                 | get all members   | None                                                           | Returns list of all dicts of members |
| GET    | "/member/{id}"            | get member by id  | `{"member_id": ...}`                                           | Returns dict of one member by id     |
| PUT    | "/member/{id}"            | update member     | `{"member_id": ..., "data": {"name": "...", "email": "..."} }` | Returns the updated member           |
| PUT    | "/member/{id}/deactivate" | deactivate member | `{"member_id": ...}`                                           | Returns the updated member           |
| PUT    | "/member/{id}/activate"   | activate member   | `{"member_id": ...}`                                           | Returns the updated member           |

---

### Reports Endpoints

| Method | Endpoint                  | Description        | Request Body       | Response                                                                                                        |
|--------|---------------------------|--------------------|--------------------|-----------------------------------------------------------------------------------------------------------------|
| GET    | "/reports/summary"        | get summary report | None               | Return dict like that: {"total_books": 0,"available_books": 0,"currently_borrowed": 0,"active_members": 0 }     |
| GET    | "/reports/books-by-genre" | count by genre     | `{"genre": "..."}` | Return list of dicts of genres like that `[{"Genre": "Science", "COUNT": 3},{"Genre": "History", "COUNT": 2}]`  |
| GET    | "/reports/top-member"     | get top member     | None               | Return dict like that: {"member_id": 1, "borrowed": 5}                                                          |

---

## System Flow

1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Borrowing a Book:**
   - User sends PATCH request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message

---

## Installation

1. Clone the repository:
```bash
https://github.com/Elazar4489/library_api.git
```

2. Navigate to the project directory:
```bash
cd C:\Users\elazar
```

3. Install dependencies:
```bash
pip indtall mysql.connector-python
pip indtall fastapi uvicorn
pip indtall logging
```

4. Set up the database:
```bash
docker exec -it mysql_libraey mysql -uroot -proot
USE libraey_db;
```

---

## Running the Project


1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and go to:
http://127.0.0.1:8000/docs
```

## Testing the API

### Test 1: Create a Member
```
POST /members
{
  "name": "Sara Cohen",
  "email": "sara@example.com"
}
```

### Test 2: Create a Book
```
POST /books
{
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "genre": "Fiction"
}
```

### Test 3: Borrow a Book
```
PATCH /books/1/borrow/1
```
