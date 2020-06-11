from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def accounts_home(request):
    return render(request, 'accounts/accounts_home.html')


