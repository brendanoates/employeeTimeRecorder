from django.conf import settings
from django.test import Client
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from profiles.models import EmployeeTimeRecorderUser as User
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
        self.USER1 = 'new.user'
        self.PASSWORD = 'testpassword'

    def tearDown(self):
        #logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_new_user_registration(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.browser.maximize_window()
        #Task C story 1 and 4
        #As a potential user I want to register on the site as a user with a unique user id and password.
        #As a user I want users to have the ability to include my staff number and managers email when registering.
        register_link = self.browser.find_element_by_id('id_register')
        register_link.click()
        self.assertEquals(self.browser.title, 'Registration')
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_staff_number = self.browser.find_element_by_id('id_staff_number')
        user_manager_email = self.browser.find_element_by_id('id_manager_email')
        user_id.send_keys(self.USER1)
        user_password.send_keys(self.PASSWORD)
        user_staff_number.send_keys('12345')
        user_manager_email.send_keys('manager.name')
        response = user_password.send_keys(Keys.ENTER)
        self.assertEquals(self.browser.title, 'Home')
        self.assertIn('welcome {}'.format(self.USER1), self.browser.find_element_by_id('menu').text)
        #Task C story 3
        #As the maintainer of the site I want a log any time a new users registers containing their IP address to help me
        #identify inappropriate usage of registration.
        last_line = ''
        with open('{}/logs/{}debug.log'.format(settings.BASE_DIR, datetime.utcnow().strftime('%y%m%d'))) as log:
            for line in log:
                last_line = line
        self.assertIn('new user: {} added, IP: '.format(self.USER1), last_line)
        #Task C story 2
        #As a registering user if my username is already in use I want to be informed.
        logout_link = self.browser.find_element_by_id('id_logout')
        logout_link.click()
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.browser.maximize_window()
        register_link = self.browser.find_element_by_id('id_register')
        register_link.click()
        self.assertEquals(self.browser.title, 'Registration')
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(self.USER1)
        user_password.send_keys(self.PASSWORD)
        response = user_password.send_keys(Keys.ENTER)
        self.assertIn('This username has already been taken', self.browser.find_element_by_id('error_msg').text)

    def test_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.browser.maximize_window()
        self.assertEquals(self.browser.title, 'Login')
        #Task C story 5
        #As a registered user I want to be able to log in
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys('userNonStaff')
        user_password.send_keys('testpassword')
        user_password.send_keys(Keys.ENTER)
        self.assertEquals(self.browser.title, 'Home')
        logout_link = self.browser.find_element_by_id('id_logout')
        logout_link.click()
        #Task C story 6
        #As a registered staff user I want to be able to log in and access the admin backend
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.browser.maximize_window()
        self.assertEquals(self.browser.title, 'Login')
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys('userStaff')
        user_password.send_keys('testpassword')
        user_password.send_keys(Keys.ENTER)
        self.assertEquals(self.browser.title, 'Home')
        self.browser.find_element_by_id('id_admin').click()
        self.assertEquals(self.browser.title, 'Site administration | Django site admin')
        #Task C7.	As a logged in user I want to be able to change my staff number and managers email

        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))


def create_users():
    testUsers = [('userNonStaff', False, False), ('userStaff', True, False,), ('userSuper', True, True)]
    for user in testUsers:
        created_user, created = User.objects.get_or_create(username=user[0], is_staff = user[1])
        created_user.is_superuser = user[2]
        created_user.set_password('testpassword')
        created_user.save()