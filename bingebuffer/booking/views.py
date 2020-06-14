from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.

@login_required(login_url="/accounts/login")
def booking_home(request):
    return render(request, 'booking/booking_home.html')

@login_required(login_url="/accounts/login")
def booking_search(request):
    searchQuery = request.POST['searchQuery']
    requestUrl = "http://www.omdbapi.com/?s={}&apikey=497974d4".format(searchQuery)
    response = requests.get(requestUrl)
    data = response.json()
    return render(request, 'booking/booking_home.html', {'movieList': data.get('Search')})


@login_required(login_url="/accounts/login")
def booking_detail(request, id):
    requestUrl = "http://www.omdbapi.com/?i={}&apikey=497974d4".format(id)
    response = requests.get(requestUrl)
    data = response.json()
    return render(request, 'booking/booking_detail.html', {'movie': data})

