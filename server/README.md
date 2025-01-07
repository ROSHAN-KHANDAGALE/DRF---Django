# Event Management Portal

## Overview

The Event Management Portal is a comprehensive solution for managing events, ticket bookings, and user interactions. It supports user authentication, QR code-based ticketing, promo code validation, and automated email notifications. Designed for both admins and users, the portal ensures seamless event registration and management.

## Features

### User Roles

- Admin:

  - Event Registration and Management.
  - Viewing booked tickets.

- User:
  - Event discovery and registration.
  - Ticket booking with QR code generation.
  - Promo code application.

## Functional Highlights

1. Event Management:

   - Admins can create, view, and manage events.
   - Each event tracks total seats and dynamically updates available seats.

2. Ticket Booking:

   - Users can book tickets for events.
   - A unique ticket ID and QR code are generated for each booking.
   - Seat availability is validated in real-time.

3. Promo Code Validation:

   - Users can apply promo codes for discounts.
   - Promo codes are validated for expiration and usage limits.

4. Email Notifications:

   - Ticket booking confirmation emails are sent to users.
   - Emails include ticket details and a QR code.

5. Authentication:
   - Custom User model supports additional fields like phone number.
   - Secure login, registration, and session management.

<hr>

## Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- PostgreSQL or SQLite

### Steps

1. Clone the Repository:

   ```
   git clone https://github.com/your-repository/event-management.git
   cd event-management
   ```

2. Install Dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Setup Database:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the Server:

   ```
   python manage.py runserver
   ```

5. Access the Portal:
   Open http://localhost:8000 in your browser.

<hr>

## Models

### User Model

Extends Django’s `AbstractUser` to include:

- `phone_number`: Optional field for additional contact information.

### Event Model

- `name`, `description`, `date`, `time`, `venue`.

- `total_seats` and `available_seats` to manage capacity.

### Ticket Model

- `ticket_id`: Randomly generated 5-7 digit unique identifier.

- `seat_number`: Number of seats booked by the user.

- `qr_code`: QR code image generated during ticket creation.

### PromoCode Model

- `code`: Unique promo code string.

- `discount`: Percentage discount offered.

- `expiry_coupon`: Expiration date of the promo code.

<hr>

## QR Code Generation

QR codes are generated using the `qrcode` library. Each ticket includes details like:

- Ticket ID

- Event Name

- User Info

- Seat Number

The QR code image is saved in the `qr_codes` directory within the media root.

<hr>

## Email Notifications

Ticket booking confirmation emails are sent via the `send_mail` function. Emails include:

- Event details (name, date, time, venue).

- Ticket ID and seat number.

- A link or attachment to the QR code.

Example Template

```
Subject: Your Ticket Booking Confirmation

Dear {username},

Thank you for booking your ticket for the event "{event_name}"!

Here are your ticket details:
Ticket ID: {ticket_id}
Event: {event_name}
Date: {event_date}
Time: {event_time}
Venue: {event_venue}
Seat Number: {seat_number}

Warm regards,
Event Management Team
```

<hr>

## API Endpoints

### Event Management

- GET /events/: List all events.

- POST /events/: Create a new event (Admin only).

### Ticket Management

- GET /tickets/: List all tickets.

- POST /tickets/: Book a ticket.

### Promo Code Validation

- POST /promocode/validate/: Validate and apply a promo code.

<hr>

## Validation Logic

- Promo Codes:

  - Expiry is checked against the current date.

  - Usage limits are enforced during application.

- Seat Availability:

  - Ensures the number of seats requested does not exceed available seats.

<hr>

## Future Enhancements

1. Payment Integration: Add support for online payment gateways.

2. Dashboard: A detailed user and admin dashboard for analytics.

3. Notifications: SMS notifications for ticket confirmations.

4. Mobile App: Extend functionality to iOS and Android apps.

<hr>

## Contribution

1. Fork the repository.

2. Create a feature branch.

3. Submit a pull request with a detailed description of your changes.

<hr>

## License

This project is licensed under the MIT License. See the LICENSE file for details.

<hr>
