from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistration,
    UserLogin,
    UserLogout,
    EventRegistration,
    TicketRegistration,
    PromoCodeView,
    StripeView,
)
from rest_framework_simplejwt.views import TokenRefreshView


# Create your URLS here
router = DefaultRouter()
router.register("auth/user/register", UserRegistration, basename="register")
router.register("auth/user/login", UserLogin, basename="login")
router.register("auth/logout", UserLogout, basename="logout")
router.register("event/booking", EventRegistration, basename="booking")
router.register("event/ticket/booking", TicketRegistration, basename="ticket")
router.register("event/Promocode/discounts", PromoCodeView, basename="promocode")
router.register("event/payment", StripeView, basename="payment")
urlpatterns = [
    path("refreshToken/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
