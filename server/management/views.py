# Imports
from django.conf import settings
from .templates import send_ticket_confirmation_email
from .models import User, Ticket, Event, PromoCode, Payment
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    EventSerializer,
    TicketSerializer,
    PromoSerializer,
    PaymentSerializer,
)

# Rest Framework imports
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Stripe imports
import stripe


# Create your views here.
# User Registration
class UserRegistration(GenericViewSet):
    user = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                f"Something went wrong: {e}", status=status.HTTP_404_NOT_FOUND
            )


# User Login
class UserLogin(GenericViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                f"Something went wrong: {e}", status=status.HTTP_404_NOT_FOUND
            )


# User Logout
class UserLogout(GenericViewSet):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Logout Successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"Something went wrong: {e}", status=status.HTTP_404_NOT_FOUND
            )


# Event Registration
class EventRegistration(GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        try:
            event = Event.objects.all()
            serializer = self.serializer_class(event, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                print(request.user)
                event = serializer.save()
                send_ticket_confirmation_email(
                    user_email=request.user.email,
                    ticket=event,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Ticket Registration
class TicketRegistration(GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            tickets = Ticket.objects.all()
            serializer = self.serializer_class(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                send_ticket_confirmation_email(
                    user_email=request.user.email,
                    ticket=event,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Promo Code Registration
class PromoCodeView(GenericViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoSerializer

    def list(self, request):
        try:
            tickets = PromoCode.objects.all()
            serializer = self.serializer_class(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Stripe Payment
class StripeView(GenericViewSet):
    serializer_class = PaymentSerializer

    def create(self, request):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            data = request.data
            amount = data.get("amount")
            currency = data.get("currency", "usd")
            payment_method = data.get("payment_method")
            user = request.user

            # Convert amount to cents
            amount_in_cents = int(float(amount) * 100)

            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency=currency,
                payment_method=payment_method,
                confirmation_method="manual",
                confirm=True,
                receipt_email=user.email,
                return_url="http://127.0.0.1:8000/payment-return",
            )

            payment_data = {
                "user": user.id,
                "amount": amount,
                "payment_intent_id": payment_intent["id"],
                "status": payment_intent["status"],
                "currency": currency,
            }

            serializer = self.serializer_class(
                data=payment_data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "payment_intent": payment_intent,
                        "payment_details": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.CardError as e:
            return Response(
                {"error": f"Card declined: {e.error.message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except stripe.error.InvalidRequestError as e:
            return Response(
                {"error": f"Invalid parameters: {e.error.message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
