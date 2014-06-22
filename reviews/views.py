

import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ReviewForm
from .models import Review
from quests.models import Quests
from users.contrib import user_handler
from users.models import QuestrUserProfile


# Create your views here.


# @login_required
# def render_review(request, quest_id, reviewed_id):
#     pagetype="review"
#     user = request.user
#     if not user_handler.userExists(reviewed_id):
#         return redirect('mytrades')

#     try:
#         current_quest = Quests.objects.get(id=quest_id)
#     except Quests.DoesNotExist:
#         raise Http404
#         return render('404.html', locals())

#     try:
#         shipper = QuestrUserProfile.objects.get(id=reviewed_id)
#         full_name = shipper.get_full_name()
#     except QuestrUserProfile.DoesNotExist:
#         raise Http404
#         return render('404.html', locals())

#     try:
#         reveiw = Review.objects.get(quest=current_quest, reviewed=shipper)
#     except Review.DoesNotExist:
#         return render(request, 'questrReview.html', locals())
#     message="The shipper has already been review"
#     return render(request,'homepage.html', locals())

@login_required
def review(request, quest_id, reviewed_id):
    if request.method == "POST":
        """
        update the shipper review from the offerer
        calculate the final rating
        """
        ratings = request.POST.getlist('rating')
        try:
            questdetails = Quests.objects.get(id=quest_id)
        except Quests.DoesNotExist:
            raise Http404
            return render(request,'404.html')
        try:
            reviewed = QuestrUserProfile.objects.get(id=reviewed_id)
        except QuestrUserProfile.DoesNotExist:
            raise Http404
            return render(request,'404.html')
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.quest_id=questdetails.id
            review.reviewed_id=reviewed.id
            review.rating_1=float(ratings[0])
            review.rating_2=float(ratings[1])
            review.rating_3=float(ratings[2])
            review.rating_4=float(ratings[3])
            review.save()
            logging.debug("Review done by {0} on quest with id {1} which was complted by shipper {2}".format(request.user, quest_id, reviewed.get_full_name()))
            return redirect('home')
    try:
        current_quest = Quests.objects.get(id=quest_id)
    except Quests.DoesNotExist:
        raise Http404
        return render('404.html', locals())

    try:
        shipper = QuestrUserProfile.objects.get(id=reviewed_id)
        full_name = shipper.get_full_name()
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render('404.html', locals())
    try:
        is_reviewed = Review.objects.get(quest=current_quest, reviewed=shipper)
    except Review.DoesNotExist:
        is_reviewed=False
        return render(request, 'questrReview.html', locals())
    return redirect('home')



