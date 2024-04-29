from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth import get_user


class RegistrationTestCase(TestCase):
    
    def test_user_account_si_created(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'Behruz',
                'first_name':'Behruz',
                'last_name':'Xoliqberdiyev',
                'email':'xoliqberdiyevbehruz@gmail.com',
                'password':'somepassword'
            }
        )
        user = CustomUser.objects.get(username='Behruz')
        self.assertEqual(user.first_name, 'Behruz')
        self.assertEqual(user.last_name, 'Xoliqberdiyev')
        self.assertEqual(user.email, 'xoliqberdiyevbehruz@gmail.com')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))

    def test_user_fields_required(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name':'Behruz',
                'last_name':'Xoliqberdiyev',
                'email':'xoliqberdiyevbehruz@gmail.com',
                'password':''
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_user_email_invalid(self):
        response = self.client.post(
                reverse('users:register'),
            data={
                'username':'Behruz',
                'first_name':'Behruz',
                'last_name':'Xoliqberdiyev',
                'email':'invalid-email',
                'password':'somepassword'
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


    def test_unique_username(self):
        user = CustomUser.objects.create(
            username='Behruz', 
            first_name='Behruz', 
            last_name='Xoliqberdiyev', 
            email='sapme@fmakd.cp'
        )
        user.set_password('somepasswrod')
        user.save()
        

        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'Bilol',
                'first_name':'Behruz',
                'last_name':'Xoliqberdiyev',
                'email':'xoliqberdiyevbehruz@gmail.com',
                'password':'somepassword',
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 2)
        self.assertNotEqual(user.username, 'Bilol')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='Behruz', first_name='Behruz')
        self.db_user.set_password('somepass')
        self.db_user.save()

    def test_succesful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": 'Behruz',
                "password": 'somepass',
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username':'wrong-username',
                'password':"somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username':'Behruz',
                'password':"wrong-pass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='Behruz', password='somepass')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username='Behruz',
            first_name='Behruz',
            last_name='Xoliqberdiyev',
            email='xoliqberdiyevbehruz@gmail.com',
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='Behruz', password='somepass')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)        

    def test_updated_profile(self):
        user = CustomUser.objects.create(
            username='Behruz',
            first_name='Behruz',
            last_name='Xoliqberdiyev',
            email='xoliqberdiyevbehruz@gmail.com',
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='Behruz', password='somepass')

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username':'Behruz',
                'first_name':'Behruz',
                'last_name':'Doe',
                'email':'xoliqberdiyev@gmail.com'

            })
        user = CustomUser.objects.get()

        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'xoliqberdiyev@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))