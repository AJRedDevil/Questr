

import logging
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from users.models import QuestrUserProfile, UserToken
from quests.models import QuestToken

def verified(a_view):
	""" 
	email verification decorator; redirects with to the home page with verfication message.
	"""
	def _wrapped_function(request, *args, **kwargs):
		if request.user.is_authenticated():
			email = request.user
			try:
				user = QuestrUserProfile.objects.get(email=email)
				if user :
					if user.email_status:
						pagetype="emailnotverified"
						return a_view(request, *args, **kwargs)
					else:
						pagetype="emailnotverified"
						request.session['alert_message'] = dict(type="warning",message="Please check your inbox and verify your email !")
						alert_message = request.session['alert_message']
						return render(request, 'thankyou.html', locals())
				success = False
				message = "User not Found"
				return render(request, 'thankyou.html', locals())
			except QuestrUserProfile.DoesNotExist:
				return render(request,'error_pages/something_broke.html', locals())
		return redirect('signin')
	return _wrapped_function

def is_alive(a_view):
	"""
	checks whether the token is alive or dead
	"""
	def _wrapped_function(request, *args, **kwargs):
		questr_token = request.GET['questr_token']
		if questr_token:
			try:
				token = UserToken.objects.get(token = questr_token)
				# check whether the token is alive and take dedcision
				if token:
					if token.is_alive():
						return a_view(request, *args, **kwargs)
					else:
						success = False
						request.session['alert_message'] = dict(type="warning",message="The link has expired please click below to request again!")
						alert_message = request.session['alert_message']
						return render(request, 'verification.html', locals())
			except UserToken.DoesNotExist:
				success = False
				request.session['alert_message'] = dict(type="danger",message="Invalid Request !")
				alert_message = request.session['alert_message']
				return render(request, 'verification.html', locals())
		else:
			return render(request,'error_pages/something_broke.html', locals())
	return _wrapped_function

def is_quest_alive(a_view):
	"""
	checks whether the token is alive or dead
	"""
	def _wrapped_function(request, *args, **kwargs):
		quest_token = request.GET['quest_token']
		if quest_token:
			try:
				token = QuestToken.objects.get(token_id = quest_token)
				# check whether the token is alive and take dedcision
				if token:
					if token.is_alive():
						return a_view(request, *args, **kwargs)
					else:
						success = False
						request.session['alert_message'] = dict(type="warning",message="The link has expired, and perhaps some other courier has been selected!")
						alert_message = request.session['alert_message']
						return redirect('home')
			except QuestToken.DoesNotExist:
				success = False
				request.session['alert_message'] = dict(type="danger",message="Invalid Request !")
				alert_message = request.session['alert_message']
				return render(request, 'thankyou.html', locals())
		else:
			return render(request,'error_pages/something_broke.html', locals())
	return _wrapped_function

def is_superuser(a_view):
	""" 
	Checks if a user is super user
	"""
	def _wrapped_function(request, *args, **kwargs):
		if request.user.is_authenticated():
			email = request.user
			try:
				user = QuestrUserProfile.objects.get(email=email)
				if user :
					if user.is_superuser:
						logging.warn("is superuser")
						return a_view(request, *args, **kwargs)
					else:
						logging.warn("is not superuser")
						return redirect('home')
				success = False
				return redirect('home')
			except QuestrUserProfile.DoesNotExist:
				return render(request,'error_pages/something_broke.html', locals())
		return redirect('signin')
	return _wrapped_function

def is_signup_token_alive(a_view):
	"""
	checks whether the token is alive or dead
	"""
	def _wrapped_function(request, *args, **kwargs):
		questr_token = request.GET['questr_token']
		if questr_token:
			try:
				token = UserToken.objects.get(token = questr_token)
				# check whether the token is alive and take dedcision
				if token:
					if token.is_alive():
						return a_view(request, *args, **kwargs)
					else:
						success = False
						request.session['alert_message'] = dict(type="warning",message="The link has expired please contact us to request again!")
						alert_message = request.session['alert_message']
						return redirect('index')
			except UserToken.DoesNotExist:
				success = False
				request.session['alert_message'] = dict(type="danger",message="Invalid Request !")
				alert_message = request.session['alert_message']
				return redirect('index')
		else:
			return render(request,'error_pages/something_broke.html', locals())
	return _wrapped_function
