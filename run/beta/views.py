from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from beta.models import Contact

def index(request):
    return render(request, 'beta/index.html')

# def is_valid_email():
	
def join_beta(request):
	new_user = Contact( email = request.POST['email'])
	new_user.save()
	return HttpResponseRedirect(reverse('beta:thankyou'))
	
def thankyou(request):
    return render(request, 'beta/thankyou.html')
