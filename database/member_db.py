from enum import member

from database.db_connection import get_connection
# from routes.member_routes import memberdb


class MemberDB:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor(dictionary=True)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        return "connection is closed"

    def create_member(self, data):
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        sql = (
            "INSERT INTO members (`name`, `email`, `is_active`, `total_borrows`) VALUES (%s, %s, TRUE, 0);")
        tp = (data["name"], data["email"])
        self.cursor.execute(sql, tp)
        self.connection.commit()
        self.cursor.execute("SELECT MAX(`id`) FROM members;")
        member_id = self.cursor.fetchone()["MAX(`id`)"]
        return self.get_member_by_id(member_id)

    def get_all_members(self):
        sql = ("SELECT * FROM members")
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_member_by_id(self, member_id):
        sql = ("SELECT * FROM members WHERE `id` = %s")
        self.cursor.execute(sql, (member_id,))
        the_member = self.cursor.fetchall()
        if the_member:
            return the_member[0]
        return None


    def update_member(self, member_id, data):
        if not self.get_member_by_id(member_id):
            raise NameError
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        sql = ("UPDATE members SET `name` = %s, `email` = %s WHERE `id` = %s")
        tp = (data["name"], data["email"], member_id)
        self.cursor.execute(sql, tp)
        self.connection.commit()
        member_updated = self.get_member_by_id(member_id)
        return member_updated

    def deactivate_member(self, member_id):
        if not self.get_member_by_id(member_id):
            raise NameError
        sql = ("UPDATE members SET `is_active` = FALSE WHERE `id` = %s")
        self.cursor.execute(sql, (member_id,))
        member_updated = self.get_member_by_id(member_id)
        self.connection.commit()
        return member_updated

    def activate_member(self, member_id):
        if not self.get_member_by_id(member_id):
            raise NameError
        sql = ("UPDATE members SET `is_active` = TRUE WHERE `id` = %s")
        self.cursor.execute(sql, (member_id,))
        member_updated = self.get_member_by_id(member_id)
        self.connection.commit()
        return member_updated

    def increment_borrowed(self,member_id):
        the_member = self.get_member_by_id(member_id)
        if not the_member:
            raise NameError
        total = the_member["total_borrows"] + 1
        sql = ("UPDATE members SET `total_borrows` = %s WHERE `id` = %s")
        self.cursor.execute(sql, (total, member_id))
        increment_bo = self.get_member_by_id(member_id)
        self.connection.commit()
        return increment_bo

    def count_active_members(self):
        sql = ("SELECT COUNT(*) AS `active_members` FROM members WHERE `is_active` = TRUE;")
        self.cursor.execute(sql)
        return self.cursor.fetchone()["active_members"]

    def get_top_member(self):
        sql = ("SELECT id, total_borrows FROM members order by total_borrows desc limit 1")
        self.cursor.execute(sql)
        return self.cursor.fetchall()








    def chack_data(self, data: dict) -> bool:
        list_of_keys = ["name", "email"]
        for key in list_of_keys:
            if key not in data:
                raise KeyError
        return True




