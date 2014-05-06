

import logging
from django.shortcuts import render
from users.models import QuestrUserProfile, QuestrToken

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
						return a_view(request, *args, **kwargs)
					else:
						return render(request, 'verification.html', locals())
				success = False
				message = "User not Found"
				return render(request, 'verification.html', locals())
			except QuestrUserProfile.DoesNotExist:
				return render(request,'error_pages/something_broke.html', locals())
		return render(request, 'login.html', locals())
	return _wrapped_function

def is_alive(a_view):
	"""
	checks whether the token is alive or dead
	"""
	def _wrapped_function(request, *args, **kwargs):
		questr_token = request.GET['questr_token']
		if questr_token:
			try:
				token = QuestrToken.objects.get(token_id = questr_token)
				# check whether the token is alive and take dedcision
				if token:
					if token.is_alive():
						logging.warn("Alive")
						return a_view(request, *args, **kwargs)
					else:
						success = False
						message = "Your token has expired."
						return render(request, 'verification.html', locals())
			except QuestrToken.DoesNotExist:
				success = False
				message = "Sorry Imposter"
				return render(request, 'verification.html', locals())
		else:
			return render(request,'error_pages/something_broke.html', locals())
	return _wrapped_function
