from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from booking.models import Booking, Bookingmeta
import uuid
import io
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table

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

@login_required(login_url="/accounts/login")
def dashboard_ticket_pdf(request, id):
    data = Bookingmeta.objects.get(transaction_id=id)
    response = HttpResponse('application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Ticket_Confirmation.pdf'
    cm = 2.54
    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)
    elements = []
    data=[('Movie Name',data.movie_name),('Screen Name',data.screen_name), ('Date', data.show_date), ('Show Time', data.show_time), ('Seats', data.seats)]
    table = Table(data, colWidths=270, rowHeights=79)
    elements.append(table)
    doc.build(elements) 
    return response
