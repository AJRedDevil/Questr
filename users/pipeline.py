from django.shortcuts import render, redirect

from social.pipeline.partial import partial

import logging

@partial
def required_fields(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email and user.first_name and user.last_name:
        return
    elif is_new:
        required_fields = ['first_name', 'last_name' , 'username','email',
                            'biography', 'phone']
        __all_present = True
        for field in required_fields:
            if not strategy.session_get(field):
                __all_present = False
        if __all_present:
            for field in required_fields:
                details[field] = strategy.session_pop(field)
            return
        else:
            kwargs['request'].session['details'] = details
            return redirect('saveprofile')


def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    USER_FIELDS = ['username', 'email', 'first_name', 'last_name']

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