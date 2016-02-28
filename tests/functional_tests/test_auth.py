from django.contrib.auth.models import User
a = User.objects.all()[0]
a.is_superuser

from django.test import Client
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import datetime, timedelta

# These will be required when WebDriverWait is used to wait for pages to load.
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

class UserAuthAdminTestCase(StaticLiveServerTestCase):
    """
    This test has been created for the completion of task b
    """
    def setUp(self):
        create_users()
        self.browser = webdriver.Chrome()
        # self.browser.implicitly_wait(10) # Wait for up to 10 seconds for the page to load.

    def tearDown(self):
        #logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        self.browser.maximize_window()

        #Task b Story 1
        # As a staff user I want log into the system and access the admin section of the project
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys('userStaff')
        user_password.send_keys('testpassword')
        user_password.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEquals(self.browser.title, 'Site administration | Django site admin')
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        #Task b Story 2
        # As a super user I want log into the system and access the admin section of the project
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys('userSuper')
        user_password.send_keys('testpassword')
        user_password.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEquals(self.browser.title, 'Site administration | Django site admin')
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        #Task b Story 3
        # As a normal user I want log into the system but be able to access the admin section of the Login of staff
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys('userNonStaff')
        user_password.send_keys('testpassword')
        user_password.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEquals(self.browser.title, 'Log in | Django site admin')
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))


class normalUser(StaticLiveServerTestCase):
    def setUp(self):
        create_users()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10) # Wait for up to 10 seconds for the page to load.

    def tearDown(self):
        #logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.browser.maximize_window()
        self.assertEquals(self.browser.title, 'login')
        #Login of staff
        # user_id = self.browser.find_element_by_id('id_username')
        # user_password = self.browser.find_element_by_id('id_password')
        # user_id.send_keys('userStaff')
        # user_password.send_keys('testpassword')
        # user_password.send_keys(Keys.ENTER)
        # time.sleep(3)
        # self.assertEquals(self.browser.title, 'Site administration | Django site admin')
        # self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))


def create_users():
    testUsers = [('userNonStaff', False, False), ('userStaff', True, False,), ('userSuper', True, True)]
    for user in testUsers:
        created_user, created = User.objects.get_or_create(username=user[0],
                                                           password='pbkdf2_sha256$24000$msczUFpPDQ5d$LbfB4LWUPYBs1Z61'
                                                                    'ATojQvEngkPqk9SafZSGL9qjZCA=',
                                                           is_staff = user[1]
                                                           )
        created_user.is_superuser = user[2]
        created_user.save()