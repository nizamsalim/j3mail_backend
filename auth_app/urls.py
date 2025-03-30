from django.urls import path
from .views import Signup, PublicKey, EmailCheck, Logout, Login, PrivateKey

urlpatterns = [
    path("signup/", Signup.as_view(), name="Signup"),
    path("login/", Login.as_view(), name="Login"),
    path("logout/", Logout.as_view(), name="Logout"),
    path("public_key/", PublicKey.as_view(), name="PublicKey"),
    path("private_key/", PrivateKey.as_view(), name="PrivateKey"),
    path("email_check/", EmailCheck.as_view(), name="EmailCheck"),
]
