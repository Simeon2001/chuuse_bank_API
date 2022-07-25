from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .account_gen import generate
from django.contrib.auth import authenticate
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = User
minimum_deposit = 500 * 100

@api_view(["post"])
@permission_classes([AllowAny])
def create_account(request):
    if request.method == "POST":
        account_number = generate()
        account_name = request.data.get("account_name")
        deposit = int(request.data.get("deposit"))
        amount = deposit * 100
        password = request.data.get("password")
        if UserModel.objects.filter(account_name__icontains=account_name).first() or minimum_deposit > amount:
            return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "name already taken by another user or your minimum deposit is should be atleast 500 naira",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            data = {'account_name': account_name, 'account_number': account_number, 'deposit': deposit,'password': password}
            serializer_class = UserSerializer(data=data)
            serializer_class.is_valid(raise_exception=True)
            data = serializer_class.save()
            return Response( {"responsecode": 201,"success": True,"message": "your account have been created"}, status=status.HTTP_201_CREATED)

@api_view(["post"])
def authr_token(request):
    if request.method == "POST":
        account_name = request.data.get("account_name")
        password = request.data.get("password")
        try:
            log = authenticate(account_name=account_name, password=password)
            refresh = RefreshToken.for_user(log)
            return Response({"responsecode":200,"success": True, "accesstoken": str(refresh.access_token),},status=status.HTTP_200_OK)
        except AttributeError:
            return Response({"responsecode":401,"success": False,"message": "Please enter the correct username and password",},status=status.HTTP_401_UNAUTHORIZED)