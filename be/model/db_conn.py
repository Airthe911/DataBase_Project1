from model import store


class DBConn:
    def __init__(self):
        self.conn = store.get_db_conn()
        self.conn["new_order"].create_index([("payment_time", 1)], expireAfterSeconds=3600)
        self.conn["new_order_detail"].create_index([("payment_time", 1)], expireAfterSeconds=3600)
        self.conn["book"].create_index([("title", "text"), ("book intro", "text"), ("content", "text"), ("tags", "text")])

    def user_id_exist(self, user_id):
        cur = self.conn["user"]
        result = cur.find({'user_id': user_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cur = self.conn["store"]
        result = cur.find({"store_id": store_id, "book_id": book_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cur = self.conn["user_store"]
        result = cur.find({"store_id": store_id})
        count = result.count()
        if count == 0:
            return False
        else:
            return True
