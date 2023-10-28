from model import store


class DBConn:
    def __init__(self):
        self.conn = store.get_db_conn()

    # def user_id_exist(self, user_id):
    #     cursor = self.conn.execute(
    #         "SELECT user_id FROM user WHERE user_id = ?;", (user_id,)
    #     )
    #     row = cursor.fetchone()
    #     if row is None:
    #         return False
    #     else:
    #         return True

    def user_id_exist(self, user_id):
        cur = self.conn["user"]
        result = cur.find({'user_id': user_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True

    # def book_id_exist(self, store_id, book_id):
    #     cursor = self.conn.execute(
    #         "SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;",
    #         (store_id, book_id),
    #     )
    #     row = cursor.fetchone()
    #     if row is None:
    #         return False
    #     else:
    #         return True

    def book_id_exist(self, store_id, book_id):
        cur = self.conn["store"]
        result = cur.find({"store_id": store_id, "book_id": book_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True

    # def store_id_exist(self, store_id):
    #     cursor = self.conn.execute(
    #         "SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,)
    #     )
    #     row = cursor.fetchone()
    #     if row is None:
    #         return False
    #     else:
    #         return True

    def store_id_exist(self, store_id):
        cur = self.conn["user_store"]
        result = cur.find({"store_id": store_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True
