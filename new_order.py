# 载入所需的包
import sqlite3
import pymongo
import uuid
import random  # 引入random模块


def data_construct(order_id, user_id, store_id):  
    one_data = {  
        "order_id": order_id,
        "user_id": user_id,
        "store_id": store_id
    }  
    return one_data


# 数据库初始化连接

# 垃圾sqlite初始化
sqlite_db = sqlite3.connect("./fe/data/be.db")
cur_s = sqlite_db.cursor()

# 芒果初始化
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['bookstore']
cur_m = db['new_order']

# 查询所有的user-store组合
sql = "select user_id, store_id from user_store"
user_store_pairs = set(cur_s.execute(sql).fetchall())

# 查询所有可能的store_id
all_stores = set([item[0] for item in cur_s.execute("select distinct store_id from user_store").fetchall()])

books_data = []  # 储存即将插入mongo的数据

# 对于每一个user_id，选择一个与其不匹配的store_id
for user_id, own_store_id in user_store_pairs:
    available_stores = all_stores - {own_store_id}  # 排除掉自己拥有的店铺
    chosen_store_id = random.choice(list(available_stores))
    
    order_id = str(uuid.uuid4())  # 为每条数据生成一个新的UUID
    books_data.append(data_construct(order_id, user_id, chosen_store_id))

cur_m.insert_many(books_data)
