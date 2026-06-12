import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "root",
        database = "library_db"
    )
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL,
        genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other") NOT NULL,
        is_available BOOLEAN NOT NULL,
        borrowed_by_member_id INT
        );
    """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        is_active BOOLEAN NOT NULL,
        total_borrows INT
        );
        """
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "table books and tablet members created"

