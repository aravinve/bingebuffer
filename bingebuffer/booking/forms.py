from django import forms
from . import models


class ShowSelection(forms.ModelForm):
    class Meta:
        model = models.Bookingmeta
        fields = ['screen_name', 'screen_location', 'show_time', 'show_date', 'movie_name', 'seats_count']

class SeatSelection(forms.ModelForm):
    class Meta:
        model = models.Bookingmeta
        fields = ['seats']