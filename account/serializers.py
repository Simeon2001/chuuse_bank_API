from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
        new_token = Token.objects.create(user=user)
        return Response(
                {
                    "responsecode": 201,
                    "success": True,
                    "message": "{0} your account have been created".format(user.account_name),
                },
            )

    class Meta:
        model = User
        fields = ["account_name", "account_number", "deposit", "password"]