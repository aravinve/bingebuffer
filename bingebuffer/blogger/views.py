from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

@login_required(login_url="/accounts/login")
def blogger_home(request):
    return render(request, 'blogger/blogger_home.html')

@login_required(login_url="/accounts/login")
def blogger_page(request, page=1, dataType='now_playing'):
    requestUrl = "https://api.themoviedb.org/3/movie/{}?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US&page={}".format(dataType,page)
    response = requests.get(requestUrl)
    data = response.json()
    request.session['page'] = page;
    request.session['dataType'] = dataType;
    return render(request, 'blogger/blogger_page.html', {'movieList': data.get('results'), 'dataType': dataType})


@login_required(login_url="/accounts/login")
def blogger_detail(request, id):
    requestUrl = "https://api.themoviedb.org/3/movie/{}?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US".format(id)
    response = requests.get(requestUrl)
    data = response.json()
    page =  request.session.get('page')
    dataType = request.session.get('dataType')
    return render(request, 'blogger/blogger_detail.html', {'movie': data, 'page': page, 'dataType': dataType})


