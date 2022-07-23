import threading

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self, account_name, account_number, deposit, password=None, **extra_fields
    ):
        if not account_name:
            raise ValueError(_("Users must have an account name"))
        if not account_number:
            raise ValueError(_("User must have account number"))
        if not deposit:
            raise ValueError(_("Users must have a deposit"))
        if password is None:
            raise ValueError(_("Users must have a Password"))
        user = self.model(
            account_name=account_name,
            account_number=account_number,
            deposit=deposit,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, account_name, account_number, deposit, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields.get("is_staff"):
            raise ValueError(_("staff must be set to true"))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must be set to true"))
        user = self.create_user(
            account_name, account_number, deposit, password, **extra_fields
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User Basic Details
    account_name = models.CharField(_("Account_name"), max_length=100, unique=True)
    account_number = models.CharField(_("Account_number"), max_length=10, unique=True)
    deposit = models.IntegerField(_("Deposit"), max_length=15, blank=True)
    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "account_name"
    REQUIRED_FIELDS = ["account_number", "deposit"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
