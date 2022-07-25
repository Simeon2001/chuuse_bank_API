from django.shortcuts import render
from .models import Transaction
from account.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

def accounts_details(request,acc_no):
    

def statement(request,acc_no):
    user = request.user
    current_user = User.object.get(account_number=acc_no)
    transact = Transaction.objects.filter(user=current_user)

    return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "name already taken by another user or your minimum deposit is should be atleast 500 naira",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

def 