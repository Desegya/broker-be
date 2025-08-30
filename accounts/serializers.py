from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "phone_number", "country"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        UserProfile.objects.create(
            user=user,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            country=validated_data.get("country", ""),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    balance_converted = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["user", "balance", "balance_converted"]

    def get_balance_converted(self, obj):
        request = self.context.get("request")
        currency = request.query_params.get("currency", "USD") if request else "USD"
        if currency == "USD":
            return obj.balance
        converted = obj.convert_balance(currency)
        return converted if converted is not None else "Conversion error"
