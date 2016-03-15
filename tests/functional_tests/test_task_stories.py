from contextlib import contextmanager
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from claims.models import Claim, ClaimType
from profiles.models import EmployeeTimeRecorderUser
from tests.functional_tests import PASSWORD, HR_USER, SUPER_USER, USER1, MANAGER2


def populate_database():
    """
    Populate the test database with the test data
    """
    content_type = ContentType.objects.get_for_model(Claim)
    try:
        auth_claim = Permission.objects.create(codename='authorise_claim',
                                  name='Can authorise claim',
                                  content_type=content_type)
    except IntegrityError:
        pass  # already added
    try:
        senior_auth_claim = Permission.objects.create(codename='senior_authorise_claim',
                                  name='Can senior authorise claim',
                                  content_type=content_type)
    except IntegrityError:
        pass  # already added

    """
    Create known about claim types
    """
    claims = {'Part Time Overtime': False, 'Weekday Overtime': False, 'Sunday Bank Holiday Overtime': False,
              'Bank Holiday Hours': False, 'Weekday On Call': False, 'On Call Weekend': False, 'On Call Bank'
                                                                                               'Holiday': False,
              'Shift A': True, 'Shift B': True, 'Shift C': True, 'Shift D': True, 'Shift E': True,
              'Shift F': True}
    for key in claims.keys():
        c = ClaimType.objects.create_claim_type(name=key, count=claims.get(key))
        c.save()

    """
    Create Groups
    """
    perm = Permission.objects.get(name='Can change claim type')
    hr_group = Group.objects.create(name='Human Resources')
    hr_group.permissions.add(perm)
    hr_group.save()

    manager_group = Group.objects.create(name='Managers')
    manager_group.permissions.add(auth_claim)
    manager_group.save()

    senior_manager_group = Group.objects.create(name='Senior Managers')
    senior_manager_group.permissions.add(senior_auth_claim)
    senior_manager_group.permissions.add(auth_claim)
    senior_manager_group.save()

    """
    Create Test Users
    """

    user = EmployeeTimeRecorderUser.objects.create_superuser(username='Super.user', email='test@email.com',
                                                             password=PASSWORD)
    user.set_password(PASSWORD)
    user.save()

    user = EmployeeTimeRecorderUser.objects.create(username='HR', email='test@email.com')
    user.groups.add(hr_group)
    user.is_staff = True
    user.set_password(PASSWORD)
    user.save()

    manager1 = EmployeeTimeRecorderUser.objects.create(username='Manager1', email='test@email.com')
    manager1.set_password(PASSWORD)
    manager1.groups.add(manager_group)
    manager1.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Manager2', email='test@email.com')
    user.set_password(PASSWORD)
    user.groups.add(manager_group)
    user.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Manager3', email='test@email.com')
    user.set_password(PASSWORD)
    user.groups.add(manager_group)
    user.save()


    user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager1', email='test@email.com')
    user.set_password(PASSWORD)
    user.groups.add(senior_manager_group)
    user.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager2', email='test@email.com')
    user.set_password(PASSWORD)
    user.groups.add(senior_manager_group)
    user.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager3', email='test@email.com')
    user.set_password(PASSWORD)
    user.groups.add(senior_manager_group)
    user.save()

    normal_user1 = EmployeeTimeRecorderUser.objects.create(username='Normal.user1', email='test@email.com')
    normal_user1.set_password(PASSWORD)
    normal_user1.manager_email = manager1.username
    normal_user1.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Normal.user2', email='test@email.com')
    user.set_password(PASSWORD)
    user.save()

    user = EmployeeTimeRecorderUser.objects.create(username='Normal.user3', email='test@email.com')
    user.set_password(PASSWORD)
    user.save()

    for x in range(1,21):
        claim = Claim(type= ClaimType.objects.all()[0], owner= normal_user1, authorising_manager=manager1,
                      date= datetime(2016,1,x), value=1)
        claim.save()



class TaskTestCases(StaticLiveServerTestCase):
    # fixtures = ['fixtures_for_test.json']

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def setUp(self):
        populate_database()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # logout
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))
        self.browser.quit()

    '''
    Task B test cases
    '''

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
        # As a normal user I want log into the system but not be able to access the admin section
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))
        user_id = self.browser.find_element_by_id('id_username')
        user_password = self.browser.find_element_by_id('id_password')
        user_id.send_keys(USER1)
        user_password.send_keys(PASSWORD)
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Log in | Django site admin')))
        self.browser.get('{}{}'.format(self.live_server_url, '/admin/logout/'))


    def test_task_C(self):
        '''
        Task C test cases
        '''
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out'))
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
        user_id.send_keys('new.user')
        user_password.send_keys(PASSWORD)
        user_staff_number.send_keys('12345')
        user_manager_email.send_keys('manager.name')
        user_password.send_keys(Keys.ENTER)
        self.assertTrue(WebDriverWait(self.browser, 10).until(ec.title_is('Home')))
        self.assertIn('welcome new.user', self.browser.find_element_by_id('bs-navbar-collapse-1').text)
        # Task C story 3
        # As the maintainer of the site I want a log any time a new users registers containing their IP address to help
        # me identify inappropriate usage of registration.
        last_line = ''
        with open('{}/logs/{}debug.log'.format(settings.BASE_DIR, datetime.utcnow().strftime('%y%m%d'))) as log:
            for line in log:
                last_line = line
        self.assertIn('new user: new.user added, IP: ', last_line)
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
        # test_login
        self.browser.get('{}{}'.format(self.live_server_url, ''))
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

        # test_profile_update
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
        action_chains = ActionChains(self.browser)
        action_chains.double_click(self.browser.find_element_by_id('id_manager_email')).perform()
        self.browser.find_element_by_id('id_manager_email').send_keys(MANAGER2)
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


    def test_task_D(self):
        '''
        Task D test cases
        '''
        # Task D story 1
        # As a HR member I want to be able to add new claim types via admin
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out'))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))
        self.browser.find_element_by_id('id_username').send_keys(HR_USER)
        self.browser.find_element_by_id('id_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_admin')))
        self.browser.find_element_by_id('id_admin').click()
        WebDriverWait(self.browser, 10).until(ec.title_is('Site administration | Django site admin'))
        self.assertIn('Claim types', self.browser.find_element_by_class_name('model-claimtype').text)
        # Task D story 2
        # As a logged in employee I want to be able to add a new claim
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out'))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))
        self.browser.find_element_by_id('id_username').send_keys(USER1)
        self.browser.find_element_by_id('id_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'new_claim_button')))
        self.browser.find_element_by_id('new_claim_button').click()
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_authorising_manager')))
        self.browser.find_element_by_id('id_date').send_keys('11 March 2016')
        self.browser.find_element_by_id('id_type').click()
        self.browser.find_element_by_id('id_type').send_keys(Keys.ARROW_DOWN)
        self.browser.find_element_by_id('id_type').click()
        self.browser.find_element_by_id('id_value').send_keys('1')
        self.browser.find_element_by_id('id_save_claim_button').click()
        # todo need to add a test to ensure we are now on correct page following an add claim
        # Task D story 3
        # As a logged in employee I want to be able to see a list of my saved claims.
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/logout/'))
        WebDriverWait(self.browser, 10).until(ec.title_is('Logged Out'))
        self.browser.get('{}{}'.format(self.live_server_url, ''))
        WebDriverWait(self.browser, 10).until(ec.title_is('Login'))
        self.browser.find_element_by_id('id_username').send_keys(USER1)
        self.browser.find_element_by_id('id_password').send_keys(PASSWORD)
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'view_claims_button')))
        self.browser.find_element_by_id('view_claims_button').click()
        WebDriverWait(self.browser, 10).until(ec.title_is('Claims View'))
        # if there are more than 14 claims I want pagination
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_next_page')))
        self.assertTrue((ec.text_to_be_present_in_element((By.ID, 'id_next_page'), 'next')))
        self.browser.find_element_by_id('id_next_page').click()
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((By.ID, 'id_previous_page')))
        # I want to display a view of my claim when I click on it in the list
