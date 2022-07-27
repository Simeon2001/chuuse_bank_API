from django.db import models
from account.models import User

# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    type = models.CharField(max_length=11, blank=False)
    narration = models.TextField(max_length=30, blank=False)
    amount = models.IntegerField(default=0)
    account_balance = models.IntegerField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.account_name
