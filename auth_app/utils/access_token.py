from auth_app.models import User
import jwt
from django.conf import settings
from utils.db import MongoDB
from bson import ObjectId

db = MongoDB().db("users")

JWT_SECRET = settings.SECRET_KEY
JWT_ALGO = "HS256"

def generate_access_token(user_id:str):
    access_token = jwt.encode(payload={"_id":user_id},key=JWT_SECRET,algorithm=JWT_ALGO)
    return access_token

def verify_access_token(access_token):
    try:
        payload = jwt.decode(access_token,JWT_SECRET,algorithms=[JWT_ALGO])
        db_user = db.find_one({"_id":ObjectId(payload["_id"])})
        user = User(db_user["_id"],db_user["email"],db_user["name"],db_user["password"])
        return user
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    