from rest_framework import serializers
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            account_name=validated_data["account_name"],
            account_number=validated_data["account_number"],
            deposit=validated_data["deposit"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = ["account_name", "account_number", "deposit", "password"]
