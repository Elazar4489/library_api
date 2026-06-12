from db_connection import get_connection


class MemberDB:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        return "connection is closed"
