from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from booking.models import Booking, Bookingmeta
import uuid

# Create your views here.
@login_required(login_url="/accounts/login")
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')


@login_required(login_url="/accounts/login")
def dashboard_feed(request):
    return render(request, 'dashboard/dashboard_feed.html')


@login_required(login_url="/accounts/login")
def dashboard_profile(request):
    return render(request, 'dashboard/dashboard_profile.html')


@login_required(login_url="/accounts/login")
def dashboard_bookings(request):
    transactions_ids = []
    results = []
    datas = Booking.objects.filter(user=request.user)
    for data in datas:
        transactions_ids.append(data.booking_meta)
    for transaction_id in transactions_ids:
        key = uuid.UUID(str(transaction_id))
        results.append(Bookingmeta.objects.get(transaction_id=key))
    return render(request, 'dashboard/dashboard_content.html', {'results': results})

@login_required(login_url="/accounts/login")
def dashboard_settings(request):
    return render(request, 'dashboard/dashboard_settings.html')