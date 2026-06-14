from database.db_connection import get_connection
class TooMuchBooks(Exception):
    pass

class BookDB:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor(dictionary=True)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        return "connection is closed"

    def create_book(self, data: dict) -> dict | None:
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        except ValueError:
            raise ValueError
        sql = ("INSERT INTO books (`title`, `author`, `genre`, `is_available`, `borrowed_by_member_id`) VALUES (%s, %s, %s, TRUE, NULL);")
        tp = (data["title"], data["author"], data["genre"])
        self.cursor.execute(sql, tp)
        self.connection.commit()
        sql = ("SELECT MAX(`id`) FROM books;")
        self.cursor.execute("SELECT MAX(`id`) FROM books;")
        book_id = self.cursor.fetchone()["MAX(`id`)"]
        return self.get_book_by_id(book_id)

    def get_all_books(self):
        sql = ("SELECT * FROM books")
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        sql = ("SELECT * FROM books WHERE `id` = %s")
        self.cursor.execute(sql, (book_id,))

        the_book = self.cursor.fetchall()
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
        sql = ("UPDATE books SET `title` = %s, `author` = %s, `genre` = %s WHERE `id` = %s")
        tp = (data["title"], data["author"], data["genre"], book_id)
        self.cursor.execute(sql, tp)
        self.connection.commit()
        book_updated = self.get_book_by_id(book_id)
        return book_updated

    def set_available(self,book_id: int, val: str, member_id: int):
        the_book = self.get_book_by_id(book_id)
        if not the_book:
            raise NameError
        if val == "borrowed":
            if the_book["is_available"] == False:
                raise KeyError
            if self.count_active_borrows_by_member(member_id) > 2:
                raise TooMuchBooks

            sql = ("UPDATE books SET `is_available` = FALSE ,`borrowed_by_member_id` = %s WHERE `id` = %s")
            self.cursor.execute(sql, (member_id, book_id))

        elif val == "return":
            if the_book["is_available"] == True:
                raise KeyError
            elif the_book["borrowed_by_member_id"] != member_id:
                raise ValueError
            sql = ("UPDATE books SET `is_available` = TRUE ,`borrowed_by_member_id` = NULL WHERE `id` = %s")
            self.cursor.execute(sql, (book_id,))
        self.connection.commit()
        the_book = self.get_book_by_id(book_id)
        return the_book


    def count_total_books(self):
        self.cursor.execute("SELECT COUNT(*) AS `all_books` FROM books")
        return self.cursor.fetchone()["all_books"]

    def count_available_books(self):
        self.cursor.execute("SELECT COUNT(*) AS `available_books` FROM books WHERE `is_available` = TRUE")
        return self.cursor.fetchone()["available_books"]

    def count_borrowed_books(self):
        self.cursor.execute("SELECT COUNT(*) AS `borrowed_books` FROM books WHERE `is_available` = FALSE")
        return self.cursor.fetchone()["borrowed_books"]



    def count_by_genre(self, genre):
        sql = (
            """
            SELECT `genre` , COUNT(`id`) AS 'the_genre'
            FROM books 
            WHERE `genre` = %s
            GROUP BY genre;
            """)
        self.cursor.execute(sql, (genre,))
        by_genre = self.cursor.fetchall()
        if not by_genre:
            raise ValueError
        return by_genre[0]

    def count_active_borrows_by_member(self, member_id):
        sql = ("SELECT COUNT(*) AS b FROM books WHERE borrowed_by_member_id = %s")
        self.cursor.execute(sql, (member_id,))
        return self.cursor.fetchall()[0]["b"]

    def chack_data(self, data: dict) -> bool:
        list_of_genres = [ "Fiction" , "Non-Fiction" , "Science" , "History" , "Other"]
        list_of_keys = ["title", "author", "genre"]
        for key in list_of_keys:
            if key not in data:
                raise KeyError
        if data["genre"] not in list_of_genres:
            raise ValueError
        return True
