

from random import choice


def get_random_password():
	"""
	Generates a random password.
	"""
	random_password = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(7)])
	return random_password