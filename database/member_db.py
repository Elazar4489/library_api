
from database.db_connection import GetConnection

class MemberDB:
    def __init__(self):
        self.connection = GetConnection()

    def create_member(self, data):
        try:
            self.chack_data(data)
        except KeyError:
            raise KeyError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = (
            "INSERT INTO members (`name`, `email`, `is_active`, `total_borrows`) VALUES (%s, %s, TRUE, 0);")
        tp = (data["name"], data["email"])
        cursor.execute(sql, tp)
        conn.commit()
        cursor.execute("SELECT MAX(`id`) FROM members;")
        member_id = cursor.fetchone()["MAX(`id`)"]
        cursor.close()
        conn.close()
        return self.get_member_by_id(member_id)

    def get_all_members(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT * FROM members")
        cursor.execute(sql)
        all_members = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_members

    def get_member_by_id(self, member_id):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT * FROM members WHERE `id` = %s")
        cursor.execute(sql, (member_id,))
        the_member = cursor.fetchall()
        cursor.close()
        conn.close()
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
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("UPDATE members SET `name` = %s, `email` = %s WHERE `id` = %s")
        tp = (data["name"], data["email"], member_id)
        cursor.execute(sql, tp)
        conn.commit()
        member_updated = self.get_member_by_id(member_id)
        cursor.close()
        conn.close()
        return member_updated

    def deactivate_member(self, member_id):
        if not self.get_member_by_id(member_id):
            raise NameError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("UPDATE members SET `is_active` = FALSE WHERE `id` = %s")
        cursor.execute(sql, (member_id,))
        member_updated = self.get_member_by_id(member_id)
        conn.commit()
        cursor.close()
        conn.close()
        return member_updated

    def activate_member(self, member_id):
        if not self.get_member_by_id(member_id):
            raise NameError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("UPDATE members SET `is_active` = TRUE WHERE `id` = %s")
        cursor.execute(sql, (member_id,))
        member_updated = self.get_member_by_id(member_id)
        conn.commit()
        cursor.close()
        conn.close()
        return member_updated

    def increment_borrows(self, member_id):
        the_member = self.get_member_by_id(member_id)
        if not the_member:
            raise NameError
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        total = the_member["total_borrows"] + 1
        sql = ("UPDATE members SET `total_borrows` = %s WHERE `id` = %s")
        cursor.execute(sql, (total, member_id))
        increment_bo = self.get_member_by_id(member_id)
        conn.commit()
        cursor.close()
        conn.close()
        return increment_bo

    def count_active_members(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT COUNT(*) AS `active_members` FROM members WHERE `is_active` = TRUE;")
        cursor.execute(sql)
        active_members = cursor.fetchone()["active_members"]
        cursor.close()
        conn.close()
        return active_members

    def get_top_member(self):
        conn = self.connection.get_conn()
        cursor = conn.cursor(dictionary=True)
        sql = ("SELECT id, total_borrows FROM members order by total_borrows desc limit 1")
        cursor.execute(sql)
        top_member = cursor.fetchall()
        cursor.close()
        conn.close()
        return top_member

    def chack_data(self, data: dict) -> bool:
        list_of_keys = ["name", "email"]
        for key in list_of_keys:
            if key not in data:
                raise KeyError
        return True




