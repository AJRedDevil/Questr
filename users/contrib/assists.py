

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from .models import QuestrUserProfile, UserTransactional, QuestrToken
from .forms import QuestrUserChangeForm, QuestrUserCreationForm, QuestrLocalAuthenticationForm, QuestrSocialSignupForm, CreatePasswordForm
import logging

from access.requires import verified, is_alive

