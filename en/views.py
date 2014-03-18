from django.shortcuts import render
from django.http import HttpResponse
from en.models import Location, User, Quest, OfferBid, Offer, QuestBid, Review
from django.utils import timezone

def index(request):
    return HttpResponse("Questr.co Index")

def user(request, user_id):
    user_obj = User.objects.get(pk=user_id)
    offer_list = user_obj.offer_set.all()
    context = {'user_obj': user_obj}
    return render(request, 'en/user.html', context)
