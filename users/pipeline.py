import logging
import json
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
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
    defaultQuestrProfileImage=settings.STATIC_URL+'img/default.png'
    if strategy.backend.name == 'facebook':
        profile = User.objects.get(email=user)
        try:
            url = 'http://graph.facebook.com/{0}?fields=picture'.format(response['id'])
            response = request('GET', url)
            response.raise_for_status()
            data = json.loads(response.content)
            ppIsDefault = data['picture']['data']['is_silhouette']
            if not ppIsDefault:
                ppUrl = data['picture']['data']['url']
                # This is done temporary, once we have S3 available we'd be using the below
                # profilePic = request('GET', ppUrl)
                # profile.avatar_file_name.save(__get_avatar_file_name(profile),
                #                            ContentFile(profilePic.content))
                profile.avatar_file_name=ppUrl
                profile.save()
            else:
                profile.avatar_file_name=defaultQuestrProfileImage
                profile.save()
        except HTTPError:
            pass
    if strategy.backend.name == 'twitter':
        profile = User.objects.get(email=user)
        try:
            ppIsDefault = response.get('default_profile_image')
            if not ppIsDefault:
                ppUrl = response.get('profile_image_url', '').replace('_normal', '')
                response = request('GET', ppUrl)
                response.raise_for_status()
                # This is done temporary, once we have S3 available we'd be using the below
                # profile.avatar_file_name.save(__get_avatar_file_name(profile),
                #                        ContentFile(response.content))
                profile.avatar_file_name=ppUrl
                profile.save()
            else:
                profile.avatar_file_name=defaultQuestrProfileImage
                profile.save()
        except HTTPError:
            pass
    if strategy.backend.name == 'google-oauth2':
        profile = User.objects.get(email=user)
        # setting user's profile picture to default incase of google plus as it doesn't provide
        # any way to check if the user has a default profile pic or not
        profile.avatar_file_name=defaultQuestrProfileImage
        profile.save()