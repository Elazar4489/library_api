from database.db_connection import GetConnection
class TooMuchBooks(Exception):
    pass

class BookDB:
    def __init__(self):
        self.connection = GetConnection()

    def create_book(self, data: dict) -> dict | None:
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        except ValueError:
            raise ValueError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("INSERT INTO books (`title`, `author`, `genre`, `is_available`, `borrowed_by_member_id`) VALUES (%s, %s, %s, TRUE, NULL);")
        tp = (data["title"], data["author"], data["genre"])
        cursor.execute(sql, tp)
        conn.commit()
        cursor.execute("SELECT MAX(`id`) FROM books;")
        book_id = cursor.fetchone()["MAX(`id`)"]
        cursor.close()
        conn.close()
        return self.get_book_by_id(book_id)

    def get_all_books(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT * FROM books")
        cursor.execute(sql)
        all_books = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_books

    def get_book_by_id(self, book_id):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT * FROM books WHERE `id` = %s")
        cursor.execute(sql, (book_id,))

        the_book = cursor.fetchall()
        cursor.close()
        conn.close()
        if the_book:
            return the_book[0]
        return None

    def update_book(self, book_id, data):
        if not self.get_book_by_id(book_id):
            raise NameError
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        except ValueError:
            raise ValueError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("UPDATE books SET `title` = %s, `author` = %s, `genre` = %s WHERE `id` = %s")
        tp = (data["title"], data["author"], data["genre"], book_id)
        cursor.execute(sql, tp)
        conn.commit()
        book_updated = self.get_book_by_id(book_id)
        cursor.close()
        conn.close()
        return book_updated

    def set_available(self,book_id: int, val: str, member_id: int):
        the_book = self.get_book_by_id(book_id)
        if not the_book:
            raise NameError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        if val == "borrowed":
            if the_book["is_available"] == False:
                raise KeyError
            if self.count_active_borrows_by_member(member_id) > 2:
                raise TooMuchBooks

            sql = ("UPDATE books SET `is_available` = FALSE ,`borrowed_by_member_id` = %s WHERE `id` = %s")
            cursor.execute(sql, (member_id, book_id))

        elif val == "return":
            if the_book["is_available"] == True:
                raise KeyError
            elif the_book["borrowed_by_member_id"] != member_id:
                raise ValueError
            sql = ("UPDATE books SET `is_available` = TRUE ,`borrowed_by_member_id` = NULL WHERE `id` = %s")
            cursor.execute(sql, (book_id,))
        conn.commit()
        the_book = self.get_book_by_id(book_id)
        cursor.close()
        conn.close()
        return the_book


    def count_total_books(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS `all_books` FROM books")
        total_books = cursor.fetchone()["all_books"]
        cursor.close()
        conn.close()
        return total_books

    def count_available_books(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS `available_books` FROM books WHERE `is_available` = TRUE")
        available_books = cursor.fetchone()["available_books"]
        cursor.close()
        conn.close()
        return available_books

    def count_borrowed_books(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS `borrowed_books` FROM books WHERE `is_available` = FALSE")
        borrowed_books = cursor.fetchone()["borrowed_books"]
        cursor.close()
        conn.close()
        return borrowed_books



    def count_by_genre(self, genre):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = (
            """
            SELECT `genre` , COUNT(`id`) AS 'the_genre'
            FROM books 
            WHERE `genre` = %s
            GROUP BY genre;
            """)
        cursor.execute(sql, (genre,))
        by_genre = cursor.fetchall()
        cursor.close()
        conn.close()
        if not by_genre:
            raise ValueError
        return by_genre[0]

    def count_active_borrows_by_member(self, member_id):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT COUNT(*) AS b FROM books WHERE borrowed_by_member_id = %s")
        cursor.execute(sql, (member_id,))
        active_borrows = cursor.fetchall()[0]["b"]
        cursor.close()
        conn.close()
        return active_borrows

    def chack_data(self, data: dict) -> bool:
        list_of_genres = [ "Fiction" , "Non-Fiction" , "Science" , "History" , "Other"]
        list_of_keys = ["title", "author", "genre"]
        for key in list_of_keys:
            if key not in data:
                raise KeyError
        if data["genre"] not in list_of_genres:
            raise ValueError
        return True
