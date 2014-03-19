from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return HttpResponse("Questr.co Index")
    
def join(request):
	return render(request, 'beta/index.html')