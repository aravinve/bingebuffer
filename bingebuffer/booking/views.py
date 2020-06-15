from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
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
    return render(request, 'booking/booking_shows.html', {'movie': movieData, 'backdrop': 'https://image.tmdb.org/t/p/original/{}'.format(movieData.get('backdrop_path')), 'page': page, 'dataType': dataType});


