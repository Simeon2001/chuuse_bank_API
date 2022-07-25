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

@api_view(["get"])
@permission_classes([IsAuthenticated])
def accounts_details(request,acc_no):
    current_user = request.user
    try:
        user = User.objects.get(account_number=acc_no)
        balance = user.deposit/100
        if current_user.id == user.id:
            return Response(
                    {
                        "responsecode": 200,
                        "success": True,
                        "account": {
                            "accountName": user.account_name,
                            "accountNumber": user.account_number,
                            "balance": balance
                        },
                    },
                    status=status.HTTP_200_OK,
            )
        else:
            return Response(
                    {
                        "responsecode": 401,
                        "success": False,
                        "message": "sorry not your account"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                
            )

            
    except User.DoesNotExist:
        return Response(
                    {
                        "responsecode": 404,
                        "success": False,
                        "message": "account does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                
            )
        

def statement(request,acc_no):
    user = request.user
    current_user = User.object.get(account_number=acc_no)
    transact = Transaction.objects.filter(user=current_user)
    print(transact)

    return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "name already taken by another user or your minimum deposit is should be atleast 500 naira",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

