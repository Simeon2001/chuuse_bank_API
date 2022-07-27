from numpy import real
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

@api_view(["post"])
@permission_classes([IsAuthenticated])
def deposit_funds(request):
    highest_fund = 100000000
    lowest_fund = 10000
    if request.method == "POST":
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")
        real_amount = amount * 100
        if real_amount < highest_fund and real_amount > lowest_fund:
            try:
                receiver = User.objects.get(account_number=account_number)
                new_balance = receiver.deposit + real_amount
                receiver.deposit = new_balance
                bal = new_balance / 100
                receiver.save()
                statement = Transaction.objects.create(user=receiver, type="deposit", narration="deposited funds", amount=amount, account_balance=bal)
                return Response(
                    {
                        "responsecode": 200,
                        "success": True,
                        "message": "{0} deposited in {1} account".format(
                            amount, account_number
                        ),
                    },
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {
                        "responsecode": 401,
                        "success": False,
                        "message": "account does not exist",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {
                    "responsecode": 401,
                    "success": False,
                    "message": "sorry you can't deposit is more than 1 million naira or less than 100 naira ",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
