from bson import ObjectId
from config.db import users_collection


class UserModel:

    @staticmethod
    def create_user(username, password, role):
        users_collection.insert_one({
            "username": username,
            "password": password,
            "role": role
        })

    @staticmethod
    def find_user(username):
        return users_collection.find_one({"username": username})

    @staticmethod
    def get_users():
        return list(users_collection.find({}, {"password": 0}))

    # ➕ NEW
    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})

    # ➕ NEW
    @staticmethod
    def delete_user(user_id):
        users_collection.delete_one({"_id": ObjectId(user_id)})