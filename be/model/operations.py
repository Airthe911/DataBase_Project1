import sqlite3 as sqlite
from model import error
from model import db_conn
from datetime import datetime

class Operations(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def delivery(self, order_id, store_id, store_owner_id, password):
        cur = self.conn["user"]
        # step1 验证登录信息是否正确
        result = cur.find({"user_id": store_owner_id, "password": password})
        if result.count() == 0:
            return error.error_authorization_fail()
        # step2 验证店主关系是否成立
        cur = self.conn["user_store"]
        result = cur.find({"user_id": store_owner_id, "store_id": store_id})
        if result.count() == 0:
            return 904, "当前用户不是对应店铺的店主"
        # step3 验证当前店铺是否确实存在这笔订单
        cur = self.conn["new_order"]
        result = cur.find({"order_id": order_id, "store_id": store_id})
        if result.count() == 0:
            return 905, "订单信息不匹配"
        # step4 查询当前订单的详情信息
        cur = self.conn["new_order_detail"]
        result = cur.find({"order_id": order_id})
        if result.count() == 0:
            return 906, "订单号有误"
        for each in result:
            state = each["state"]
            break
        if state != 1:
            return 907, "只有处于未发货状态才能进行发货"
        # step 5 发货
        result = cur.update_one({"order_id": order_id}, {"$set": {"state": 2, "delivery_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        if result.matched_count == 0:
            return 908, "发货时出错"
        return 200, "ok"

    def receipt(self, order_id, user_id, password):
        # step1 验证登录信息是否正确
        cur = self.conn["user"]
        result = cur.find({"user_id": user_id, "password": password})
        if result.count() == 0:
            return error.error_authorization_fail()
        # step2 验证这个用户是否确实有这个订单
        cur = self.conn["new_order"]
        result = cur.find({"user_id": user_id, "order_id": order_id})
        if result.count() == 0:
            return 905, "订单信息不匹配"
        # step3 收货
        cur = self.conn["new_order_detail"]
        result = cur.find({"order_id": order_id})
        if result.count() == 0:
            return 906, "订单号有误"
        for each in result:
            state = each["state"]
            break
        if state != 2:
            return 909, "只有处于已发货、未收货的状态，才能进行本操作"
        result = cur.update_one({"order_id": order_id}, {"$set": {"state": 3, "receipt_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        if result.matched_count == 0:
            return 910, "收货时出错"
        return 200, "ok"

    def lookup(self, order_id, user_id, password):
        # step1 验证登录信息是否正确
        cur = self.conn["user"]
        result = cur.find({"user_id": user_id, "password": password})
        if result.count() == 0:
            return error.error_authorization_fail()
        # step2 验证这个用户是否确实有这个订单
        cur = self.conn["new_order"]
        result = cur.find({"user_id": user_id, "order_id": order_id})
        if result.count() == 0:
            return 905, "订单信息不匹配"
        # step3 查询订单结果并返回
        cur = self.conn["new_order_detail"]
        result = cur.find({"order_id": order_id})
        if result.count() == 0:
            return 906, "订单号有误"
        for each in result:
            print(type(each))
            print(each)
            return 200, str(each)

    def cancer(self, order_id, user_id, password):
        # step1 验证登录信息是否正确
        cur = self.conn["user"]
        result = cur.find({"user_id": user_id, "password": password})
        if result.count() == 0:
            return error.error_authorization_fail()
        # step2 验证这个用户是否确实有这个订单
        cur = self.conn["new_order"]
        result = cur.find({"user_id": user_id, "order_id": order_id})
        if result.count() == 0:
            return 905, "订单信息不匹配"
        # step3 查询订单状态，仅仅只有未付款的订单可以取消（后续或可以增加，付款未发货的也可以取消，然后执行退款操作）
        cur = self.conn["new_order_detail"]
        result = cur.find({"order_id": order_id})
        if result.count() == 0:
            return 906, "订单号有误"
        for each in result:
            state = each["state"]
            back_book_id = each["book_id"]  # 书号
            back_count = int(each["count"])  # 购买的数量
            back_price = each["price"]  # 购买的单价
            break
        cur = self.conn["new_order"]
        result = cur.find({"order_id": order_id})
        for each in result:
            back_store_id = each["store_id"]  # 售出的商店id
            back_user_id = each["user_id"]  # 购买的用户id
            break
        if state == 0:  # 订单尚未付款,只需返还数据
            # 首先删除订单信息
            cur = self.conn["new_order_detail"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return 912, "取消订单时出错"
            cur = self.conn["new_order"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return 913, "取消订单时出错"
            # 书籍返还
            cur = self.conn["store"]
            result = cur.update_one({"store_id": back_store_id, "book_id": back_book_id}, {"$inc": {"stock_level": back_count}})
            if result.matched_count == 0:
                return 918, "返还书籍时出错"
        elif state == 1:  # 订单已付款，但尚未发货。此时需要退钱
            # 额外需要知道店主是谁
            cur = self.conn["user_store"]
            result = cur.find({"store_id": back_store_id})
            if result.count() == 0:
                return 919, "店铺不存在"
            for each in result:
                store_owner_id = each["user_id"]
                break
            # 查一下店主钱是否充足，如果店主钱不足，仍然无法完成取消订单
            cur = self.conn["user"]
            result = cur.find({"user_id": store_owner_id})
            if result.count() == 0:
                return 920, "店主不存在"
            for each in result:
                seller_balance = each["balance"]
                break
            if seller_balance < back_count * back_price:
                return 921, "店主余额不足，取消订单失败"
            else:
                result = cur.update_one({"user_id": store_owner_id}, {"$set": {"balance": seller_balance - back_count * back_price}})
                if result.matched_count == 0:
                    return 922, "退款失败"
                result = cur.update_one({"user_id": back_user_id}, {"$inc": {"balance": back_count * back_price}})
                if result.matched_count == 0:
                    return 922, "退款失败"
            # 首先删除订单信息
            cur = self.conn["new_order_detail"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return 912, "取消订单时出错"
            cur = self.conn["new_order"]
            result = cur.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return 913, "取消订单时出错"
            # 书籍返还
            cur = self.conn["store"]
            result = cur.update_one({"store_id": back_store_id, "book_id": back_book_id}, {"$inc": {"stock_level": back_count}})
            if result.matched_count == 0:
                return 918, "返还书籍时出错"
            # 退钱
        else:
            return 917, "已发货或已收货的订单无法取消"
        return 200, "ok"

    def global_search(self, keyword):
        if keyword == '':
            return 914, "搜索关键词不能为空"
        cur = self.conn["book"]
        results = cur.find({"$text": {"$search": keyword}}).limit(10)  # 分页，最多返回10条记录
        if results.count() == 0:
            return 915, "没有找到相关内容"
        return_values = ""
        for result in results:
            return_values += "标题: " + result["title"] + ", 作者: " + result["author"] + ", 介绍: " + result["book_intro"] + ", 出版年份: " + result["pub_year"] + "\n"
        return 200, return_values

    def local_search(self, keyword, store_id):
        if keyword == '':
            return 914, "搜索关键词不能为空"
        cur = self.conn["store"]
        store_info = cur.find({"store_id": store_id})
        if store_info.count() == 0:
            return 916, "该店铺不存在或没有任何在售书籍"
        book_ids = []
        for each in store_info:
            book_ids.append(each["book_id"])
        cur = self.conn["book"]
        results = cur.find({"id": {"$in": book_ids}, "$text": {"$search": keyword}}).limit(10)  # 分页，最多返回10条记录
        if results.count() == 0:
            return 915, "没有找到相关内容"
        return_values = ""
        for result in results:
            return_values += "标题: " + result["title"] + ", 作者: " + result["author"] + ", 介绍: " + result["book_intro"] + ", 出版年份: " + result["pub_year"] + "\n"
        return 200, return_values
