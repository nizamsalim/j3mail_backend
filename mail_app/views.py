from rest_framework.views import APIView
from rest_framework.response import Response
from auth_app.utils.jwt_authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
# Create your views here.

class ProtectedTest(APIView):
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[CustomJWTAuthentication]
    def get(self,req):
        user:User= req.user
        return Response({
            "success":True,
            "message":f"Hello {user.name}"
        })
