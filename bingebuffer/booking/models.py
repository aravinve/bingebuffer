from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    secret_key = models.CharField(max_length=10)
    transaction_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    movie_name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=30)
    screen_location = models.CharField(max_length=30)
    show_time = models.CharField(max_length=10)
    price = models.FloatField()
    seats = models.CharField(max_length=30)

    def __str__(self):
        return self.id;