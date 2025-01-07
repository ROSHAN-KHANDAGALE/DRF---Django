from django.core.mail import send_mail
from django.conf import settings


def send_ticket_confirmation_email(user_email, ticket):
    email_subject = "Your Ticket Booking Confirmation"
    email_body = f"""
    Dear {ticket.user.first_name} {ticket.user.last_name},

    Thank you for booking your ticket for the event "{ticket.event.name}"!

    Here are your ticket details:
    ------------------------------------------
    Ticket ID: {ticket.ticket_id}
    Event: {ticket.event.name}
    Date: {ticket.event.date.strftime('%d-%m-%Y')}
    Time: {ticket.event.time.strftime('%I:%M %p')}
    Venue: {ticket.event.venue}
    Seat Number: {ticket.seat_number}
    ------------------------------------------

    Please find the QR code for your ticket attached to this email or download it from your account on our website.

    If you have any questions or need further assistance, feel free to contact us.

    Warm regards,
    Event Management Team
    """

    send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
