from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("register/", views.create_account, name="register"),
    path("login/", views.authr_token, name="login"),

]

