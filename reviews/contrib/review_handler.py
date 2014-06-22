

import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from reviews.models import Review
from quests.models import Quests
from users.contrib import user_handler
from users.models import QuestrUserProfile

def get_review(user_id):
    allreviews = Review.objects.filter(reviewed_id=user_id).all()
    return allreviews