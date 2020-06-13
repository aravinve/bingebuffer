from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/accounts/login")
def blogger_home(request):
    return render(request, 'blogger/blogger_home.html')


