import sqlite3
import pymongo
import random

def data_construct(store_id, book_id, book_info):
    return {
        "store_id": store_id,
        "book_id": book_id,
        "book_info": book_info,
        "stock_level": random.randint(1, 1000)
    }

# 数据库初始化连接

# SQLite初始化
sqlite_db = sqlite3.connect("./fe/data/be.db")
cur_s = sqlite_db.cursor()

# MongoDB初始化
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['bookstore']

# 从SQLite获取所有的store_id
sql = "select store_id from user_store"
store_ids = [row[0] for row in cur_s.execute(sql)]

# 从MongoDB获取所有的book_id和tags作为book_info
book_collection = db['book']
books = list(book_collection.find({}, {"id": 1, "tags": 1}))

book_data = []

# 为每个store_id赋予所有的book_id
all_books_ids = {book['id'] for book in books}
store_books = {store_id: set(all_books_ids) for store_id in store_ids}

# 随机选择一些store_id并删除其中的一些book_id
selected_store_ids = random.sample(store_ids, k=int(len(store_ids) * 0.5))
for store_id in selected_store_ids:
    num_to_remove = random.randint(1, len(all_books_ids) - 1)
    books_to_remove = random.sample(list(all_books_ids), k=num_to_remove)  # Change made here
    store_books[store_id].difference_update(books_to_remove)

for store_id, book_ids in store_books.items():
    for book_id in book_ids:
        book_info = next(b['tags'] for b in books if b['id'] == book_id)
        book_data.append(data_construct(store_id, book_id, book_info))

db['store'].insert_many(book_data)
