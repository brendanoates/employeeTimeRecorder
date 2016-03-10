'''
 Unit test the registration view, must be able to register with a unique user id or receive an error response if id
 is not unique
'''


# class RegisterViewTest(TestCase):
#     STAFFNUMBER = '12345'
#     MANAGER_EMAIL = 'manager.name'
#
#     def test_registartion_page_contains_correct_html_(self):
#         client = Client()
#         response = client.get(reverse('accounts:accounts-register'))
#         self.assertTrue(response.content.startswith(b'<!doctype html>'))
#         self.assertIn(b'<title>Registration</title>', response.content)
#         self.assertIn(b'<label for="id_username">Username:</label>', response.content)
#         self.assertTrue(response.content.endswith(b'</html>'))
#
#     def test_registartion_allows_registration(self):
#         client = Client()
#         response = client.post(reverse('accounts:accounts-register'),
#                                {'username': 'testuser', 'password': 'testpassword'})
#         self.assertContains(response, '', status_code=302)
#         self.assertEqual(response.url, reverse('index'))  # should redirect to index
#         client.get(reverse('accounts:accounts-logout'))
#         response = client.post(reverse('accounts:accounts-register'),
#                                {'username': 'testuser', 'password': 'testpassword'})
#         self.assertContains(response, 'This username has already been taken', status_code=200)
#
#     def test_registration_with_staff_number_manager_email(self):
#         client = Client()
#         response = client.post(reverse('accounts:accounts-register'),
#                                {'username': 'testuser', 'password': 'testpassword', 'staff_number': self.STAFFNUMBER,
#                                 'manager_email': self.MANAGER_EMAIL})
#         self.assertContains(response, '', status_code=302)
#         self.assertEqual(response.url, reverse('index'))  # should redirect to index
#         user = User.objects.get(username='testuser')
#         self.assertEqual(user.staff_number, self.STAFFNUMBER)
#
#         self.assertEqual(user.manager_email, self.MANAGER_EMAIL)
#
#
# '''
# Unit test the login view must be able to login with valid userid and password or receive an error message.
# '''
#
#
# class LoginViewTest(TestCase):
#     USERNAME = 'testuser'
#     '''
#     create a user to test the login view
#     '''
#
#     def setUp(self):
#         client = Client()
#         client.post(reverse('accounts:accounts-register'),
#                     {'username': self.USERNAME, 'password': 'testpassword'})
#         client.get(reverse('accounts:accounts-logout'))
#
#     def test_login_page_contains_correct_html(self):
#         client = Client()
#         response = client.get(reverse('accounts:accounts-login'))
#         self.assertTrue(response.content.startswith(b'<!doctype html>'))
#         self.assertIn(b'<title>Login</title>', response.content)
#         self.assertIn(b'<label for="id_username">Username:</label>', response.content)
#         self.assertTrue(response.content.endswith(b'</html>'))
#
#     def test_login_allows_login(self):
#         client = Client()
#         response = client.post(reverse('accounts:accounts-login'),
#                                {'username': self.USERNAME, 'password': 'testpassword'})
#         self.assertContains(response, '', status_code=302)
#         self.assertEqual(response.url, reverse('index'))  # should redirect to index
#         client.get(reverse('accounts:accounts-logout'))
#         response = client.post(reverse('accounts:accounts-login'),
#                                {'username': 'failuser', 'password': 'testpassword'})
#         self.assertContains(response, "Your username and password didn't match. Please try again.", status_code=200)
#
#     def test_disabled_user_cant_sign_in(self):
#         client = Client()
#         user = User.objects.get(username=self.USERNAME)
#         user.is_active = False
#         user.save()
#         response = client.post(reverse('accounts:accounts-login'),
#                                {'username': self.USERNAME, 'password': 'testpassword'})
#         self.assertContains(response, "This account has been deactivated", status_code=200)
