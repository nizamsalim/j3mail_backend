from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from .access_token import verify_access_token
from rest_framework.request import Request
from auth_app.models import User

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request:Request):
        token = request.COOKIES.get("access_token")
        
        if not token:
            return None
        try:
            user = verify_access_token(token)
            return (user,None) if user else (AnonymousUser(),None)
        except Exception as e:
            return None