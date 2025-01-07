from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
import datetime
import random
import qrcode
import os


# Create your models here.
# Custom User Model
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/")
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.name


# QR Generator
def qr_generator(url, name=None):
    if name is None:
        name = f"QR_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.png"

    qr_path = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(qr_path, exist_ok=True)

    file_path = os.path.join(qr_path, name)
    image = qrcode.make(url)
    image.save(file_path)
    return f"qr_codes/{name}"


# Ticket Model
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=7, unique=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True)

    def __str__(self):
        return f"Ticket {self.id} for {self.event.name}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()

        if not self.qr_code:
            qr_data = (
                f"\nTicket ID: {self.ticket_id}, \nEvent: {self.event.name}, "
                f"\nUser: {self.user.username}, \nSeat: {self.seat_number}"
            )
            qr_path = qr_generator(qr_data, name=f"ticket_{self.ticket_id}.png")
            self.qr_code = qr_path

            if self.pk is None:
                if self.event.available_seats < self.seat_number:
                    raise ValueError("Seats Unavailable!!")
                self.event.available_seats -= self.seat_number
                self.event.save()

        super().save(*args, **kwargs)

    def generate_ticket_id(self):
        while True:
            ticket_id = str(random.randint(10000, 9999999))
            if not Ticket.objects.filter(ticket_id=ticket_id).exists():
                return ticket_id


# Promo Code Model
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    usage_count = models.IntegerField(default=0)
    expiry_coupon = models.DateField()

    def is_valid(self):
        if self.expiry_coupon < timezone.now().date():
            return False, "Promo code has expired."
        if self.usage_count >= self.max_usage_limit:
            return False, "Promo code usage limit reached."
        return True, "Promo code is valid."

    def promo_code_limit(self):
        self.usage_count += 1
        self.save()

    def __str__(self):
        return self.code


# Payment Model
class Payment(models.Model):
    # Status Choices
    PENDING = "processing"
    COMPLETED = "succeeded"
    FAILED = "payment_failed"

    STATUS_CHOICES = (
        (PENDING, "processing"),
        (COMPLETED, "succeeded"),
        (FAILED, "payment_failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="usd")
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_intent_id} - {self.status}"
