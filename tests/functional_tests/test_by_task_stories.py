from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from profiles.models import EmployeeTimeRecorderUser as User
from tests.functional_tests import PASSWORD, HR_USER, SENIOR_MANAGER1, SENIOR_MANAGER2 ,SUPER_USER, USER1, USER2, \
    USER3, MANAGER1, MANAGER2, MANAGER3


class TaskBTestCases(StaticLiveServerTestCase):
    """
    This class holds the tests which haves been created for the completion of task B
    """
    fixtures = ['claims.json', 'profiles.json']
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))

        # Task b Story 1
        # As a staff user I want log into the system and access the admin section of the project
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(HR_USER)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Site administration | Django site admin')))
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Logged out | Django site admin')))
        # Task b Story 2
        # As a super user I want log into the system and access the admin section of the project
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(SUPER_USER)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Site administration | Django site admin')))
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Logged out | Django site admin')))
        # Task b Story 3
        # As a normal user I want log into the system but be able to access the admin section of the Login of staff
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(USER1)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))


class TaskCTestCases(StaticLiveServerTestCase):
    """
    This class holds the tests which haves been created for the completion of task C
    """

    fixtures = ['claims.json', 'profiles.json']
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.USER1 = 'new.user'


    def tearDown(self):
        # logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_new_user_registration(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        # self.browser.maximize_window()
        # Task C story 1 and 4
        # As a potential user I want to register on the site as a user with a unique user id and password.
        # As a user I want to have the ability to include my staff number and managers email when registering.
        register_link = self.browser.find_element_by_id('id_register')
        register_link.click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Registration')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_staff_number = self.browser.find_element_by_id('id_staff_number')
        user_manager_email = self.browser.find_element_by_id('id_manager_email')
        user_id.send_keys(self.USER1)
        user_password.send_keys(PASSWORD)
        user_staff_number.send_keys('12345')
        user_manager_email.send_keys('manager.name')
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        self.assertIn('welcome {}'.format(self.USER1), self.browser.find_element_by_id('bs-navbar-collapse-1').text)
        # Task C story 3
        # As the maintainer of the site I want a log any time a new users registers containing their IP address to help
        # me identify inappropriate usage of registration.
        last_line = ''
        with open('{}/logs/{}debug.log'.format(settings.BASE_DIR, datetime.utcnow().strftime('%y%m%d'))) as log:
            for line in log:
                last_line = line
        self.assertIn('new user: {} added, IP: '.format(self.USER1), last_line)
        # Task C story 2
        # As a registering user if my username is already in use I want to be informed.
        logout_link = self.browser.find_element_by_id('id_logout')
        logout_link.click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out')))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        register_link = self.browser.find_element_by_id('id_register')
        register_link.click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Registration')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(USER1)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.text_to_be_present_in_element((By.ID, 'error_message'),
                                                                                               'This username has '
                                                                                               'already been taken')))

    def test_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        # self.browser.maximize_window()
        self.assertEquals(self.browser.title, 'Login')
        # Task C story 5
        # As a registered user I want to be able to log in
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(USER1)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        logout_link = self.browser.find_element_by_id('id_logout')
        logout_link.click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out')))
        # Task C story 6
        # As a registered staff user I want to be able to log in and access the admin backend
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Login')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(HR_USER)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        self.browser.find_element_by_id('id_admin').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Site administration | Django site admin')))

    def test_profile_update(self):
        # Task C7.	As a logged in user I want to be able to change my staff number and managers email
        self.browser.get('{}{}'.format(self.live_server_url, reverse('accounts:accounts-logout')))
        self.browser.get('{}{}'.format(self.live_server_url, reverse('accounts:accounts-login')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(USER1)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        self.browser.find_element_by_id('id_account').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Profile')))
        self.browser.find_element_by_id('id_staff_number').send_keys('54321')
        self.browser.find_element_by_id('id_manager_email').send_keys(MANAGER1)
        self.browser.find_element_by_id('update_profile_button').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        # Task C story 8
        # As a logged in user I want to be able to change my password
        self.browser.find_element_by_id('id_account').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Profile')))
        self.browser.find_element_by_id('id_change_password').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Password Change Form')))
        self.browser.find_element_by_id('id_old_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_new_password1').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_new_password2').send_keys(PASSWORD)
        self.browser.find_element_by_xpath('//input[@value="Change my password"]').click()
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Password changed')))


class TaskDTestCases(StaticLiveServerTestCase):
    """
    This class holds the tests which haves been created for the completion of task D
    """
    fixtures = ['accounts.json', 'claims.json', 'profiles.json']
    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        # logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    def test_new_user_registration(self):
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        # Task D story 1
        # As a HR member I want to be able to add new claim types via admin
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))
        self.browser.find_element_by_id('id_username').send_keys(HR_USER)
        self.browser.find_element_by_id('id_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_admin')))
        self.browser.find_element_by_id('id_admin').click()
        WebDriverWait(self.browser, 10).until(ec.title_is('Site administration | Django site admin'))
        self.assertIn(('Claim types'), self.browser.find_element_by_class_name('model-claimtype').text)
        # Task D story 2
        # As a logged in employee I want to be able to add a new claim
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged out | Django site admin'))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))
        self.browser.find_element_by_id('id_username').send_keys(USER1)
        self.browser.find_element_by_id('id_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'new_claim_button')))
        self.browser.find_element_by_id('new_claim_button').click()
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_authorising_manager')))
        self.browser.find_element_by_id('id_date').send_keys('11 March 2016')
        self.browser.find_element_by_id('id_value').send_keys('1')
        self.browser.find_element_by_id('id_save_claim_button').click()
        # Task D story 3
        # As a logged in employee I want to be able to see a list of my saved claims.
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged out | Django site admin'))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))