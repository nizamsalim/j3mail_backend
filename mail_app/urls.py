from django.urls import path
from .views import Mail, MailList, ReadMail

urlpatterns = [
    path("send/", Mail.as_view(), name="Mail"),
    path("list/", MailList.as_view(), name="MailList"),
    path("read/", ReadMail.as_view(), name="ReadMail"),
]
