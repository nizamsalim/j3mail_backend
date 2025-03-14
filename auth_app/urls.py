from django.urls import path
from .views import Signup,GetPublicKey,EmailCheck,Logout,Test,Login
"/auth/"
urlpatterns = [
    path("signup/",Signup.as_view(),name="Signup"),
    path("login/",Login.as_view(),name="Login"),
    path("logout/",Logout.as_view(),name="Logout"),
    path("test/",Test.as_view(),name="Test"),
    path("public_key/",GetPublicKey.as_view(),name="GetPublicKey"),
    path("email_check/",EmailCheck.as_view(),name="EmailCheck"),
]
