from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def blogger_home(request):
    return HttpResponse("Blogger")


