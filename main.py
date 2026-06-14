from fastapi import FastAPI
import mysql.connector
from database.db_connection import get_connection, create_tables
from routes import book_routes
from routes import member_routes
from routes import report_routes
import logging
from database import db_connection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(massage)s")
file_handler = logging.FileHandler("logs/app.log", encoding = "utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
coon = db_connection.get_connection()
tables = db_connection.create_tables()

app = FastAPI()
app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)
