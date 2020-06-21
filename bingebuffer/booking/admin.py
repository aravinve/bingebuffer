from django.contrib import admin
from .models import Booking, Bookingmeta
# Register your models here.
admin.site.register(Bookingmeta)
admin.site.register(Booking)