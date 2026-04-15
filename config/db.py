from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["supermarket"]

users_collection = db["users"]
products_collection = db["products"]
sales_collection = db["sales"]

