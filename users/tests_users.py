

import logging

from django.test import TestCase
from django.test.client import Client

from users.models import QuestrUserProfile
# from users.forms import QuestrUserCreationForm
# Create your tests here.
class SignupCase(TestCase):
    """Tests for User case"""
    def setUp(self):
        super(SignupCase, self).setUp()
        self.client = Client()
        self.username = "gaumire"
        self.first_name = "Gaurav"
        self.last_name = "Ghimire"
        self.password1 = "123456"
        self.password2 = "123456"
        self.email = "gaurav.ghimire@gmail.com"
        self.post_data={'first_name':self.first_name,'last_name':self.last_name,'displayname':self.username,\
        'password1':self.password1,'password2':self.password2,'email':self.email}                        

    def test_signup_url(self):
        response = self.client.post('/user/signup/', data=self.post_data)
        self.assertEqual(response.status_code, 200)

    # def test_signup_validated(self):
    #     response = self.client.post('/user/signup/', data=self.post_data)
    #     # print dir(response)
    #     print response.content

    def test_user_is_created(self):
        response = self.client.post('/user/signup/', data=self.post_data)
        user = QuestrUserProfile.objects.get(email=self.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.displayname, 'self.username')
    #     # pri nt response.context
