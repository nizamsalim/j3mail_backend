"""
URL configuration for j3mail_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self,req):
        return Response({
            "Application Link":"https://j3mail.vercel.app",
            "Github":{
                "Frontend":"https://github.com/nizamsalim/j3mail_frontend",
                "Backend":"https://github.com/nizamsalim/j3mail_backend",
            }
        })

urlpatterns = [
    path("",HomeView.as_view(),name="Home"),
    path('admin/', admin.site.urls),
    path("auth/",include("auth_app.urls")),
    path("mail/",include("mail_app.urls"))
]
