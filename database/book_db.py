from database.db_connection import get_connection

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

            sql = ("UPDATE books SET `is_available` = FALSE ,`borrowed_by_member_id` = %s")
            self.cursor.execute(sql, (member_id,))
        elif val == "return":
            if the_book["is_available"] == True:
                raise KeyError
                return f"the book: {the_book} is not borrowed"
            elif the_book["borrowed_by_member_id"] != member_id:
                raise ValueError
                return f"the book: {the_book} is already borrowed to someone else"
            sql = ("UPDATE books SET `is_available` = TRUE ,`borrowed_by_member_id` = NULL")
            self.cursor.execute(sql)

        the_book = self.get_book_by_id(book_id)
        return the_book







    def chack_data(self, data: dict) -> bool:
        list_of_genres = [ "Fiction" , "Non-Fiction" , "Science" , "History" , "Other"]
        list_of_keys = ["title", "author", "genre"]
        for key in list_of_keys:
            if key not in data:
                raise KeyError
        if data["genre"] not in list_of_genres:
            raise ValueError
        return True

