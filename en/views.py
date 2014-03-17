from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Questr.co Index")


# Create your views here.
