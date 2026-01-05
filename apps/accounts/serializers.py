from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)  # 🔥 REQUIRED

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "confirm_password"
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # 🔥 VERY IMPORTANT

        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data.get("name"),
            password=validated_data["password"],
        )
        return user
