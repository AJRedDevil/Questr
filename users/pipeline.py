import logging
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.utils import timezone
from requests import request, HTTPError
from social.pipeline.partial import partial
from .views import userExists, emailExists
from .models import QuestrUserProfile as User


@partial
def required_fields(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new:
        required_fields = ['first_name', 'last_name' , 'displayname', 'email']
        __all_present = True
        for field in required_fields:
            if not strategy.session_get(field):
                __all_present = False
        if __all_present:
            for field in required_fields:
                details[field] = strategy.session_pop(field)
            # redirect if user exists
            if userExists(details['displayname']):
                logging.warn("userExists")
                return redirect('saveprofile')
            # redirect if email exists
            if emailExists(details['email']):
                logging.warn("emailExists")
                return redirect('saveprofile')      

            return
        else:
            kwargs['request'].session['details'] = details
            return redirect('saveprofile') # commented for later use


def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    USER_FIELDS = ['email', 'first_name', 'last_name', 'displayname']
    if user:
        return {'is_new': False}
    fields = dict((name, kwargs.get(name) or details.get(name))
                        for name in strategy.setting('USER_FIELDS',
                                                      USER_FIELDS))
    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }

def __get_formated_datetime(_datetime):
    return _datetime.strftime("%d%m%Y%H%M%S")

def __get_avatar_file_name(profile):
    _filename = '{0}_{1}.jpg'.format(profile.id, __get_formated_datetime(profile.date_joined))
    return _filename


def save_profile_picture(strategy, user, response, details, is_new=False,*args,**kwargs):
    if strategy.backend.name == 'facebook':
        profile = User.objects.get(email=user)
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
            profile.avatar_file_name.save(__get_avatar_file_name(profile),
                                       ContentFile(response.content))
            profile.save()
            response.raise_for_status()
        except HTTPError:
            pass
