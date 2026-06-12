from fastapi import FastAPI
import mysql.connector
from database.db_connection import get_connection, create_tables
from routes import book_routes
from routes import member_routes
from routes import report_routes
app = FastAPI()
app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)

