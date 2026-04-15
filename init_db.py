from config.db import users_collection
from utils.security import hash_password

# clear old bad data (IMPORTANT)
users_collection.delete_many({})

# insert correct admin user
users_collection.insert_one({
    "username": "admin",
    "password": hash_password("1234"),
    "role": "admin"
})
# insert correct cashier user
users_collection.insert_one({
    "username": "cashier",
    "password": hash_password("1234"),
    "role": "cashier"
})

print("Clean DB + admin created+cashier")