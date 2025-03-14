from django.urls import path
from .views import ProtectedTest
urlpatterns = [
    path("protected/",ProtectedTest.as_view(),name="Protected")
]
