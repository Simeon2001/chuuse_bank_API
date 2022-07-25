from django.urls import path
from trans import views

app_name = "trans"

urlpatterns = [
    path("account_info/<str:acc_no>", views.accounts_details, name="account_info"),
#    path("login/", views.authr_token, name="login"),

]