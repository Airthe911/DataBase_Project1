import sqlite3 as sqlite
import uuid
import json
import logging
from model import db_conn
from model import error


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    # def new_order(
    #     self, user_id, store_id, id_and_count):
    #     order_id = ""
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id) + (order_id,)
    #         if not self.store_id_exist(store_id):
    #             return error.error_non_exist_store_id(store_id) + (order_id,)
    #         uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

    #         for book_id, count in id_and_count:
    #             cursor = self.conn.execute(
    #                 "SELECT book_id, stock_level, book_info FROM store "
    #                 "WHERE store_id = ? AND book_id = ?;",
    #                 (store_id, book_id),
    #             )
    #             row = cursor.fetchone()
    #             if row is None:
    #                 return error.error_non_exist_book_id(book_id) + (order_id,)

    #             stock_level = row[1]
    #             book_info = row[2]
    #             book_info_json = json.loads(book_info)
    #             price = book_info_json.get("price")

    #             if stock_level < count:
    #                 return error.error_stock_level_low(book_id) + (order_id,)

    #             cursor = self.conn.execute(
    #                 "UPDATE store set stock_level = stock_level - ? "
    #                 "WHERE store_id = ? and book_id = ? and stock_level >= ?; ",
    #                 (count, store_id, book_id, count),
    #             )
    #             if cursor.rowcount == 0:
    #                 return error.error_stock_level_low(book_id) + (order_id,)

    #             self.conn.execute(
    #                 "INSERT INTO new_order_detail(order_id, book_id, count, price) "
    #                 "VALUES(?, ?, ?, ?);",
    #                 (uid, book_id, count, price),
    #             )

    #         self.conn.execute(
    #             "INSERT INTO new_order(order_id, store_id, user_id) "
    #             "VALUES(?, ?, ?);",
    #             (uid, store_id, user_id),
    #         )
    #         self.conn.commit()
    #         order_id = uid
    #     except sqlite.Error as e:
    #         logging.info("528, {}".format(str(e)))
    #         return 528, "{}".format(str(e)), ""
    #     except BaseException as e:
    #         logging.info("530, {}".format(str(e)))
    #         return 530, "{}".format(str(e)), ""

    #     return 200, "ok", order_id

    def new_order(
        self, user_id, store_id, id_and_count):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            order_id = uid
            for book_id, count in id_and_count:
                # cursor = self.conn.execute(
                #     "SELECT book_id, stock_level, book_info FROM store "
                #     "WHERE store_id = ? AND book_id = ?;",
                #     (store_id, book_id),
                # )
                cur = self.conn["store"]
                result = cur.find({"store_id": store_id, "book_id": book_id})
                if result.count() == 0:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                for each in result:
                    stock_level = each["stock_level"]
                    break
                cur = self.conn["book"]
                result = cur.find({"id": book_id})
                if result.count() == 0:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                for each in result:
                    price = each["price"]
                    break
                # book_info_json = json.loads(book_info)
                # price = book_info_json.get("price")
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)
                # cursor = self.conn.execute(
                #     "UPDATE store set stock_level = stock_level - ? "
                #     "WHERE store_id = ? and book_id = ? and stock_level >= ?; ",
                #     (count, store_id, book_id, count),
                # )
                cur = self.conn["store"]
                result = cur.update_one({"store_id": store_id, "book_id": book_id, "stock_level": stock_level}, {"$set": {"stock_level": stock_level - count}})
                if result.matched_count == 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                # self.conn.execute(
                #     "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                #     "VALUES(?, ?, ?, ?);",
                #     (uid, book_id, count, price),
                # )
                cur = self.conn["new_order_detail"]
                result = cur.insert_one({
                    "order_id": order_id, 
                    "book_id": book_id, 
                    "count": count,
                    "price": price
                })
                if not result.acknowledged:
                    return 902, "数据插入失败"

            # self.conn.execute(
            #     "INSERT INTO new_order(order_id, store_id, user_id) "
            #     "VALUES(?, ?, ?);",
            #     (uid, store_id, user_id),
            # )
            # self.conn.commit()
            cur = self.conn["new_order"]
            result = cur.insert_one({
                "order_id": order_id,
                "store_id": store_id,
                "user_id": user_id
            })
        except sqlite.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str):
        try:
            # cursor = conn.execute(
            #     "SELECT order_id, user_id, store_id FROM new_order WHERE order_id = ?",
            #     (order_id,),
            # )
            # row = cursor.fetchone()
            cur = self.conn["new_order"]
            result = cur.find({"order_id": order_id})
            if result.count() == 0:
                return error.error_invalid_order_id(order_id)
            for each in result:
                order_id = each["order_id"]
                buyer_id = each["user_id"]
                store_id = each["store_id"]
                break

            if buyer_id != user_id:
                return error.error_authorization_fail()

            # cursor = conn.execute(
            #     "SELECT balance, password FROM user WHERE user_id = ?;", (buyer_id,)
            # )
            # row = cursor.fetchone()
            cur = self.conn["user"]
            result = cur.find({"user_id": buyer_id})
            if result.count() == 0:
                return error.error_non_exist_user_id(buyer_id)
            for each in result:
                balance = each["balance"]
                this_password = each["password"]
                break
            if password != this_password:
                return error.error_authorization_fail()

            # cursor = conn.execute(
            #     "SELECT store_id, user_id FROM user_store WHERE store_id = ?;",
            #     (store_id,),
            # )
            # row = cursor.fetchone()
            cur = self.conn["user_store"]
            result = cur.find({"store_id": store_id})
            if result.count() is None:
                return error.error_non_exist_store_id(store_id)
            for each in result:
                seller_id = each["user_id"]
                break
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            # cursor = conn.execute(
            #     "SELECT book_id, count, price FROM new_order_detail WHERE order_id = ?;",
            #     (order_id,),
            # )
            cur = self.conn["new_order_detail"]
            result = cur.find({"order_id": order_id})
            if result.count() == 0:
                return 903, "查询new_order_detail表出错"
            total_price = 0
            # for row in cursor:
            #     count = row[1]
            #     price = row[2]
            #     total_price = total_price + price * count
            for each in result:
                count = each["count"]
                price = each["price"]
                total_price = total_price + price * count
            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            # cursor = conn.execute(
            #     "UPDATE user set balance = balance - ?"
            #     "WHERE user_id = ? AND balance >= ?",
            #     (total_price, buyer_id, total_price),
            # )
            cur = self.conn["user"]
            result = cur.update_one({"user_id": buyer_id, "balance": total_price}, {"$set": {"balance": balance - total_price}})
            if cur.matched_count == 0:
                return error.error_not_sufficient_funds(order_id)
            # cursor = conn.execute(
            #     "UPDATE user set balance = balance + ?" "WHERE user_id = ?",
            #     (total_price, buyer_id),
            # )
            cur = self.conn["user"]
            result = cur.update_one({"user_id": buyer_id}, {"$set": {"balance": balance + total_price}})
            if result.matched_count == 0:
                return error.error_non_exist_user_id(buyer_id)
            # cursor = conn.execute(
            #     "DELETE FROM new_order WHERE order_id = ?", (order_id,)
            # )
            cur = self.conn["new_order"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return error.error_invalid_order_id(order_id)
    
            # cursor = conn.execute(
            #     "DELETE FROM new_order_detail where order_id = ?", (order_id,)
            # )
            cur = self.conn["new_order_detail"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return error.error_invalid_order_id(order_id)

        except sqlite.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    # def add_funds(self, user_id, password, add_value):
    #     try:
    #         cursor = self.conn.execute(
    #             "SELECT password  from user where user_id=?", (user_id,)
    #         )
    #         row = cursor.fetchone()
    #         if row is None:
    #             return error.error_authorization_fail()

    #         if row[0] != password:
    #             return error.error_authorization_fail()

    #         cursor = self.conn.execute(
    #             "UPDATE user SET balance = balance + ? WHERE user_id = ?",
    #             (add_value, user_id),
    #         )
    #         if cursor.rowcount == 0:
    #             return error.error_non_exist_user_id(user_id)

    #         self.conn.commit()
    #     except sqlite.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         return 530, "{}".format(str(e))

    #     return 200, "ok"

    def add_funds(self, user_id, password, add_value):
        try:
            # cursor = self.conn.execute(
            #     "SELECT password  from user where user_id=?", (user_id,)
            # )
            cur = self.conn["user"]
            result = cur.find({"user_id": user_id})
            if result.count() == 0:
                return error.error_authorization_fail()
            for each in result:
                saved_password = each["password"]
                balance = each["balance"]
            if saved_password != password:
                return error.error_authorization_fail()

            # cursor = self.conn.execute(
            #     "UPDATE user SET balance = balance + ? WHERE user_id = ?",
            #     (add_value, user_id),
            # )
            cur = self.conn["user"]
            result = cur.update_one({"user_id": user_id}, {"$set": {"balance": balance + add_value}})
            if result.matched_count == 0:
                return error.error_non_exist_user_id(user_id)

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"