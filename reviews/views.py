

import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Avg

from .forms import ReviewForm
from .models import Review
from quests.models import Quests
from users.contrib import user_handler
from users.models import QuestrUserProfile

logger = logging.getLogger(__name__)
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
    """Reviews a user for a quest, where reviewed_id is the id of the user being reviewed"""
    logger.debug("User being reviewed is %s", reviewed_id)
    logger.debug("User who is reviewing is %s", request.user.id)
    # If the user tries to review himself
    if int(reviewed_id)==int(request.user.id):
        return redirect('home')
    if request.method == "POST":
        """
        update the shipper review from the offerer
        calculate the final rating
        """
        # If the user tries to review himself
        if int(reviewed_id)==int(request.user.id):
            return redirect('home')

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
            logger.debug("Review done by {0} on quest with id {1} which was complted by shipper {2}".format(request.user, quest_id, reviewed.get_full_name()))
            final_rating = Review.objects.filter(reviewed=reviewed.id).aggregate(Avg('final_rating'))
            final_rating = round(final_rating['final_rating__avg'], 1)
            QuestrUserProfile.objects.filter(id=reviewed_id).update(rating=final_rating)

            # if the guy being reviewed is the questr
            # changing the types to integer for it's an integer comparision, IDs are integers
            if int(questdetails.questrs_id) == int(reviewed_id):
                logger.debug("shipper is reviewed")
                Quests.objects.filter(id=quest_id).update(is_questr_reviewed='t')

            # if the guy being reviewed is the shipper
            # changing the types to integer for it's an integer comparision, IDs are integers
            if int(questdetails.shipper) == int(reviewed_id):
                logger.debug("questr is reviewed")
                Quests.objects.filter(id=quest_id).update(is_shipper_reviewed='t')

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
        logger.debug(is_reviewed)
    except Review.DoesNotExist:
        is_reviewed=False
        return render(request, 'questrReview.html', locals())

    logger.debug("redirecting to home")    
    return redirect('home')



