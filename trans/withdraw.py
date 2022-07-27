from .models import Transaction
from account.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.contrib.auth import authenticate


@api_view(["post"])
@permission_classes([IsAuthenticated])
def withdraw_funds(request):
    if request.method == "POST":
        min_amount = 1 * 100
        max_balance = 500 * 100
        user = request.user
        account_number = request.data.get("account_number")
        password = request.data.get("password")
        withdraw_amount = request.data.get("withdraw_amount")
        amount = withdraw_amount * 100
        if amount < min_amount:
            return Response(
                {
                    "responsecode": 400,
                    "successful": False,
                    "message": "withdraw amount is less than 1 naira",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                query_user = User.objects.get(account_number=account_number)
                auth = authenticate(account_name=query_user.account_name, password=password)
                if auth:
                    if user.id != auth.id:
                        return Response(
                            {
                                "responsecode": 401,
                                "successful": False,
                                "message": "not your account",
                            },
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                    else:
                        balance = query_user.deposit - amount
                        if balance > max_balance:
                            query_user.deposit = balance
                            bal = balance / 100
                            query_user.save()
                            statement = Transaction.objects.create(user=query_user, type="withdraw", narration="withdraw funds", amount=withdraw_amount, account_balance=bal)
                            return Response(
                                {
                                    "responsecode": 200,
                                    "successful": True,
                                    "message": "{0} withdrawn from your account".format(withdraw_amount),
                                },
                                status=status.HTTP_200_OK,
                            )
                        else:
                            return Response(
                                {
                                    "responsecode": 400,
                                    "successful": False,
                                    "message": "In order to withdraw {0}, 500 naira must be left in your account".format(withdraw_amount),
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                else:
                    return Response(
                        {
                            "responsecode": 401,
                            "successful": False,
                            "message": "invalid account_number or password",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except User.DoesNotExist:
                return Response(
                            {
                                "responsecode": 404,
                                "successful": False,
                                "message": "sorry account does not exist",
                            },
                            status=status.HTTP_404_NOT_FOUND,
                        )
