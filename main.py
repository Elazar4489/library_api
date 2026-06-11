from fastapi import FastAPI
import mysql.connector
app = FastAPI()

@app.get("/")
def return_hello():
    return "hello"

conn = mysql.connector.connect(
    host= "localhost",
    user = "root",
    password = "root"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE ffoo;")
print("database created")
