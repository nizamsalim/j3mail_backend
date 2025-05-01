from rest_framework.views import APIView
from rest_framework.response import Response
from utils.db import MongoDB
from .utils.cipher import decrypt_auth_body_rsa
from django.conf import settings
from .models import SignupBody, LoginBody
from django.contrib.auth.hashers import make_password as hash, check_password
from .utils.access_token import generate_access_token


# Create your views here.

db = MongoDB().db("users")
keys = MongoDB().db("keys")


ise = {"success": False, "error": "Something went wrong", "field": "server"}

# class ClientRSAKey(API):
#     pass


class EmailCheck(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, req):
        try:
            email = req.data["email"]
            user = db.find_one({"email": email})
            res = False
            if user:
                res = True
            return Response({"success": True, "user_exists": res})
        except Exception as e:
            print(str(e))
            return Response(ise)


class PrivateKey(APIView):
    def get(self, req):
        user_id = req.user._id
        key_record = keys.find_one({"_id": user_id})
        # print(key_record)
        return Response({"success": True, "private_key": key_record["private_key"]})

    def post(self, req):
        key_pair = req.data  # publicKey, privateKey
        user_id = req.user._id
        keys.insert_one(
            {
                "_id": user_id,
                "private_key": key_pair["privateKey"],
                "public_key": key_pair["publicKey"],
            }
        )
        return Response({"success": True})


class PublicKey(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        public_key = settings.PUBLIC_KEY
        return Response({"success": True, "public_key": public_key})

    def post(self, req):
        email = req.data["email"]
        user = db.find_one({"email": email})
        # get public key of email
        key_record = keys.find_one({"_id": user["_id"]})
        return Response({"success": True, "public_key": key_record["public_key"]})


class Signup(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            encrypted_data = request.data["data"]
            decrypted_data = decrypt_auth_body_rsa(encrypted_data)
            user = SignupBody(**decrypted_data)
            # print(user)
            user_exists = db.find_one({"email": user.email})
            if user_exists:
                return Response({"success": False, "error": "Email already exists"})
            pwd_hash = hash(user.password)
            user.password = pwd_hash
            res = db.insert_one(user.__dict__)
            access_token = generate_access_token(str(res.inserted_id))
            response = Response(
                {
                    "success": True,
                    "user": {
                        "_id": str(res.inserted_id),
                        "name": user.name,
                        "email": user.email,
                    },
                }
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                max_age=3600 * 24,
                samesite="None"
            )
            return response
        except Exception as e:
            return Response({"m": str(e)}, 500)


class Login(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, req):
        try:
            encrypted_data = req.data["data"]
            user = LoginBody(**decrypt_auth_body_rsa(encrypted_data))
            db_user = db.find_one({"email": user.email})
            if not db_user:
                return Response({"success": False, "error": "Email doesnt exist"})
            password_match = check_password(user.password, db_user["password"])
            if not password_match:
                return Response({"success": False, "error": "Incorrect password"})

            access_token = generate_access_token(str(db_user["_id"]))

            response = Response(
                {
                    "success": True,
                    "user": {
                        "_id": str(db_user["_id"]),
                        "name": db_user["name"],
                        "email": db_user["email"],
                    },
                }
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=3600 * 24,
            )
            return response

        except Exception as e:
            return Response(ise)


class Logout(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, req):
        res = Response({"success": True})
        res.delete_cookie("access_token")
        return res
