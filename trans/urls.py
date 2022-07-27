from django.urls import path
from trans import views
from trans import withdraw, deposit

app_name = "trans"

urlpatterns = [
    path("account_info/<str:acc_no>", views.accounts_details, name="account_info"),
    path("statement/<str:acc_no>", views.statement, name="statement"),
    path("deposit", deposit.deposit_funds, name="deposit"),
    path("withdrawal", withdraw.withdraw_funds, name="withdraw"),
]
