from rest_framework import serializers
from .models import Transaction

class Statement_Serializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.account_name")

    class Meta:
        model = Transaction
        fields = ["transaction_date", "user", "type", "narration", "amount", "account_balance",]