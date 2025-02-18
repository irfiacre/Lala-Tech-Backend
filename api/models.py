import uuid
from django.db import models

def generate_id():
    return str(uuid.uuid4())

class Users(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('host', 'Host'),
        ('renter', 'Renter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    photo_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Properties(models.Model):
    property_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo_urls = models.JSONField(default=list, blank=True)
    host = models.ForeignKey(Users, on_delete=models.PROTECT, related_name="properties")
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('available', 'Available'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=3.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveIntegerField()
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    furnished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    property = models.ForeignKey(Properties, on_delete=models.PROTECT, related_name="bookings")
    user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name="bookings")

    STATUS_CHOICES = [
        ('canceled', 'Canceled'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    is_inappropriate = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking {self.booking_id} - {self.status}"
