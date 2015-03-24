from django.shortcuts import render, redirect
from application.forms import CourierApplyForm, UserApplyForm
from libs import onboardiq_handler as obhandler
import os
# Create your views here.
import logging
# Init Logger
logger = logging.getLogger(__name__)


def applyAsCourier(request):
    user_form = CourierApplyForm()
    pagetitle = "Apply to be a Questr courier"
    if request.method == "POST":
        logger.debug(request.POST)
        user_form = CourierApplyForm(data=request.POST)
        if user_form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken')
            data['available_days'] = ','.join(request.POST.getlist('available_days'))
            data['available_hours'] = ','.join(request.POST.getlist('available_hours'))
            data['api_token'] = os.environ['ONBOARDIQ_API_KEY']
            onboardiq = obhandler.OnboardIQConnector()
            onboardiq.sendApplicationDetail(data)
            return redirect('index')

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)

    return render(request, 'apply_courier.html', locals())


def applyAsUser(request):
    user_form = UserApplyForm()
    pagetitle = "Request invitation"
    if request.method == "POST":
        logger.debug(request.POST)
        user_form = UserApplyForm(data=request.POST)
        if user_form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken')
            data['api_token'] = os.environ['ONBOARDIQ_API_KEY']
            onboardiq = obhandler.OnboardIQConnector()
            onboardiq.sendApplicationDetail(data)
            return redirect('index')

        if user_form.errors:
            logger.debug("Form has errors, %s ", user_form.errors)
    return render(request, 'apply_user.html', locals())
