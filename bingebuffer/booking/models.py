from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Bookingmeta(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen_name = models.CharField(max_length=30)
    screen_location = models.CharField(max_length=30)
    show_time = models.CharField(max_length=10)
    show_date = models.CharField(max_length=20)
    movie_name = models.CharField(max_length=100)
    price = models.FloatField()
    seats_count = models.IntegerField()
    seats = models.CharField(max_length=30)
    

    def __str__(self):
        return self.transaction_id


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    booking_date = models.DateTimeField(auto_now_add=True)
    secret_key = models.CharField(max_length=10)
    booking_meta = models.ForeignKey(Bookingmeta, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.id;