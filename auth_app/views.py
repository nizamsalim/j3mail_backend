from rest_framework.views import APIView
from rest_framework.response import Response
from utils.db import MongoDB
from .utils.cipher import decrypt_auth_body_rsa,test
from django.conf import settings
from .models import SignupBody,LoginBody
from django.contrib.auth.hashers import make_password as hash,check_password
from .utils.access_token import generate_access_token


# Create your views here.

db = MongoDB().db("users")

ise = {
    "success":False,
    "error":"Something went wrong",
    "field":"server"
}

class Test(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self,req):
        test()
        return Response()

class EmailCheck(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,req):
        try:
            email = req.data["email"]
            user = db.find_one({"email":email})
            res = False
            if user:
                res = True
            return Response({"success":True,"user_exists":res})
        except Exception as e:
            return Response(ise)

class GetPublicKey(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self,request):
        public_key = settings.PUBLIC_KEY
        return Response({"success":True,"public_key":public_key})

class Signup(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,request):
        try:
            encrypted_data = request.data["data"]
            decrypted_data = decrypt_auth_body_rsa(encrypted_data)
            user = SignupBody(**decrypted_data)
            # print(user)
            user_exists = db.find_one({"email":user.email})
            if user_exists:
                return Response({"success":False,"error":"Email already exists"})
            pwd_hash = hash(user.password)
            user.password = pwd_hash
            res = db.insert_one(user.__dict__)
            access_token = generate_access_token(str(res.inserted_id))
            response = Response({
                "success":True,
                "user":{
                    "_id":str(res.inserted_id),
                    "name":user.name
                }
            })
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                max_age=3600*24
            )
            return response
        except Exception as e:
            return Response({"m":str(e)},500)
class Login(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,req):
        try:
            encrypted_data = req.data["data"]
            user = LoginBody(**decrypt_auth_body_rsa(encrypted_data))
            db_user = db.find_one({"email":user.email})
            if not db_user:
                return Response({"success":False,"error":"Email doesnt exist"})
            password_match = check_password(user.password,db_user["password"])
            if not password_match:
                return Response({"success":False,"error":"Incorrect password"})
            
            access_token = generate_access_token(str(db_user["_id"]))

            response = Response({
                "success":True,
                "user":{
                    "_id":str(db_user["_id"]),
                    "name":db_user["name"]
                }
            })
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                max_age=3600*24
            )
            return response

        except Exception as e:
            return Response(ise)

class Logout(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self,req):
        res = Response({"success":True})
        res.delete_cookie("access_token")
        return res