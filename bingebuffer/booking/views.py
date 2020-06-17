from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
import string
import datetime
from .models import Booking
# Create your views here.

@login_required(login_url="/accounts/login")
def booking_home(request):
    return render(request, 'booking/booking_home.html')

@login_required(login_url="/accounts/login")
def booking_page(request, page=1, dataType='now_playing'):
    requestUrl = "https://api.themoviedb.org/3/movie/{}?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US&page={}".format(dataType,page)
    response = requests.get(requestUrl)
    data = response.json()
    request.session['page'] = page;
    request.session['dataType'] = dataType;
    return render(request, 'booking/booking_page.html', {'movieList': data.get('results'), 'dataType': dataType, 'searchBox': True})


@login_required(login_url="/accounts/login")
def booking_detail(request, id):
    requestUrl = "https://api.themoviedb.org/3/movie/{}?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US".format(id)
    response = requests.get(requestUrl)
    data = response.json()
    page =  request.session.get('page')
    dataType = request.session.get('dataType')
    request.session['movieData'] = data
    return render(request, 'booking/booking_detail.html', {'movie': data, 'page': page, 'dataType': dataType, 'backdrop': 'https://image.tmdb.org/t/p/original/{}'.format(data.get('backdrop_path'))})


@login_required(login_url="/accounts/login")
def booking_imdb_detail(request, id):
    requestUrl = "http://www.omdbapi.com/?i={}&apikey=497974d4".format(id)
    response = requests.get(requestUrl)
    data = response.json()
    page =  request.session.get('page')
    dataType = request.session.get('dataType')
    return render(request, 'booking/booking_imdb_detail.html', {'movie': data,'page': page, 'dataType': dataType})


@login_required(login_url="/accounts/login")
def booking_search(request):
    searchQuery = request.POST['searchQuery']
    requestUrl = "https://api.themoviedb.org/3/search/movie?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US&query={}&page=1&include_adult=false".format(searchQuery)
    response = requests.get(requestUrl)
    data = response.json()
    request.session['page'] = 1;
    request.session['dataType'] = "now_playing";
    return render(request, 'booking/booking_page.html', {'movieList': data.get('results'), 'dataType': "now_playing", 'searchBox': False})

@login_required(login_url="/accounts/login")
def booking_shows(request, movieId):
    movieData = request.session.get('movieData')
    page =  request.session.get('page')
    dataType = request.session.get('dataType')
    SHOWS = [
        {'show_name': 'Morning', 'show_time': '09.00 AM'},
        {'show_name': 'Noon', 'show_time': '12.00 PM'},
        {'show_name': 'Matinee', 'show_time': '03.00 PM'},
        {'show_name': 'Evening', 'show_time': '06.00 PM'},
        {'show_name': 'Night', 'show_time': '10.00 PM'},
    ]
    SCREENS = [ 
        {'screen_name': 'Screen 1', 'screen_location': 'Chennai'},
        {'screen_name': 'Screen 2', 'screen_location': 'Singapore'}, 
        {'screen_name': 'Screen 3', 'screen_location': 'Sydney'}, 
        {'screen_name': 'Screen 4', 'screen_location': 'New York'},
        {'screen_name': 'Screen 5', 'screen_location': 'Dubai'}
    ]
    return render(request, 'booking/booking_shows.html', {'movie': movieData, 'backdrop': 'https://image.tmdb.org/t/p/original/{}'.format(movieData.get('backdrop_path')), 'page': page, 'dataType': dataType, 'shows': SHOWS, 'screens': SCREENS, 'seatCount': range(11)[1:11]});


def booking_seat_selection(request):
    if request.method == 'POST':
        showTime = request.POST['showTime']
        seatsCount = request.POST['seats']
        screenName = request.POST['screenName']
        screenLocation = request.POST['screenLocation']
        showDate = request.POST['showDate']
        seats = []
        for i in list(string.ascii_uppercase)[:10]:
            row = []
            for j in range(10):
                row.append('{}{}'.format(i,j+1))
            seats.append(row)
        movieData = request.session.get('movieData')
        return render(request, 'booking/booking_seat_selection.html', {'seats': seats, 'movie': movieData, 'seatsCount': seatsCount, 'showTime': showTime, 'screenName': screenName, 'screenLocation': screenLocation, 'showDate': showDate})