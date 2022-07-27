from .models import Transaction
from account.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from .serializers import Statement_Serializer

@api_view(["get"])
@permission_classes([IsAuthenticated])
def accounts_details(request, acc_no):
    current_user = request.user
    try:
        user = User.objects.get(account_number=acc_no)
        balance = user.deposit / 100
        if current_user.id == user.id:
            return Response(
                {
                    "responsecode": 200,
                    "success": True,
                    "account": {
                        "accountName": user.account_name,
                        "accountNumber": user.account_number,
                        "balance": balance,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "sorry not your account",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except User.DoesNotExist:
        return Response(
            {
                "responsecode": 404,
                "success": False,
                "message": "account does not exist",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

@api_view(["get"])
@permission_classes([IsAuthenticated])
def statement(request, acc_no):
    user = request.user
    try:
        current_user = User.objects.get(account_number=acc_no)
        if user.id == current_user.id:
            transact = Transaction.objects.filter(user=current_user)
            serializer_class = Statement_Serializer(transact, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
            
        else:
            return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "sorry not your account",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except User.DoesNotExist:
        return Response(
            {
                "responsecode": 404,
                "success": False,
                "message": "account does not exist",
            },
            status=status.HTTP_404_NOT_FOUND,
        )




