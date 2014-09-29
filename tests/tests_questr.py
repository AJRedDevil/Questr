

import unittest

from selenium import webdriver

# from django.test import TestCase
# from django.utils import timezone
# from users.models import QuestrUserProfile

class QuestrTest(unittest.TestCase):
    """Tests Questr WebApp"""

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_1(self):
        """Signup with the service"""
        self.driver.get("http://localhost:5000/user/signup")
        self.driver.find_element_by_id('email').send_keys("gaurav.ghimire@gmail.com")
        self.driver.find_element_by_id('password1').send_keys("123456")
        self.driver.find_element_by_id('password2').send_keys("123456")
        self.driver.find_element_by_id('displayname').send_keys("gaumire")
        self.driver.find_element_by_id('first_name').send_keys("Gaurav")
        self.driver.find_element_by_id('last_name').send_keys("Ghimire")
        self.driver.find_element_by_id('city').send_keys("Toronto")
        self.driver.find_element_by_id('streetaddress').send_keys("16 Brookers Lane")
        self.driver.find_element_by_id('postalcode').send_keys("M8V0A5")
        self.driver.find_element_by_id('phone').send_keys("+1234567890")
        self.driver.find_element_by_id('createAccBtn').click()
        self.driver.find_element_by_link_text('here').click()
        self.driver.get("http://localhost:5000/user/home")

    # def test_2(self):
    #     """Verify Email"""
    #     self.driver.get("http://localhost:5000/user/home")
    #     self.driver.find_element_by_id('username').send_keys("gaurav.ghimire@gmail.com")
    #     self.driver.find_element_by_id('password').send_keys("123456")
    #     self.driver.find_element_by_link_text('here').click()

    # def test_login(self):
    #     self.driver.get("http://localhost:5000/user/signin")
    #     self.driver.find_element_by_id('email').send_keys("gaurav.ghimire@gmail.com")
    #     self.driver.find_element_by_id('password').send_keys("123456")
    #     self.driver.find_element_by_id('submit').click()
    #     self.driver.get("http://localhost:5000/quest/new")
