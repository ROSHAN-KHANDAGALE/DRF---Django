from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Event, Ticket, PromoCode, Payment


# Create your Serializers here
# User Registeration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        # Create the user and set the password
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            password=password,
        )

        return user


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("INVALID CREDENTAILS")

        # Generate JWT Tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# User Logout Serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            return self.errors


# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "time",
            "venue",
            "image",
            "total_seats",
            "available_seats",
        ]


# Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    # event = EventSerializer()
    # user = RegisterSerializer()

    class Meta:
        model = Ticket
        fields = [
            "event",
            "user",
            "seat_number",
            "qr_code",
            "ticket_id",
        ]
        read_only_fields = ["qr_code", "ticket_id"]


# Promo Code Serializer
class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            "code",
            "discount",
            "usage_count",
            "expiry_coupon",
        ]


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "amount",
            "payment_intent_id",
            "status",
            "currency",
            "created_at",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("INVALID AMOUNT VALUE!!")
        return value
