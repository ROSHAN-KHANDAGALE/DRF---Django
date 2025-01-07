from django.contrib import admin
from .models import User, Event, Ticket, PromoCode, Payment

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(PromoCode)
admin.site.register(Payment)
