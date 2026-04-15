from models.user_model import UserModel
from utils.security import hash_password, check_password

class AuthController:

    # 👤 REGISTER NEW USER (ADMIN ONLY USE CASE)
    @staticmethod
    def register(username, password, role):

        username = username.strip()

        # 🚫 prevent empty inputs
        if not username or not password:
            raise ValueError("Username and password required")

        # 🚫 check if user already exists
        if UserModel.find_user(username):
            raise Exception("User already exists")

        # 🔐 hash password before saving
        hashed_password = hash_password(password)

        UserModel.create_user(username, hashed_password, role)

    # 🔐 LOGIN USER
    @staticmethod
    def login(username, password):

        username = username.strip()

        user = UserModel.find_user(username)

        # ❌ user not found
        if not user:
            return None

        # 🔐 check password
        if check_password(password, user["password"]):
            return user

        return None

    # 👥 GET ALL USERS (ADMIN FEATURE)
    @staticmethod
    def get_users():
        return UserModel.get_users()