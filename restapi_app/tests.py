from rest_framework.test import APITestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User

from profiles_app.models import ProfileModel


class APIListViewTest(APITestCase):
    first_user_data = {'password': 'MyPass2018', 'username': 'admin2', 'phone': '80055535943'}
    second_user_data = {'password': 'MyPass2018', 'username': 'admin3', 'phone': '8005553593'}
    new_data = {'short_status': 'Короткий статус', 'phone': '800555359000'}

    client = Client()

    def test_get_token(self):
        self.register_user(self.first_user_data)
        response = self.client.post(reverse('get_token'), self.first_user_data)
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.register_user(self.first_user_data)
        expected_response = {'id': 1}
        self.assertEqual(response.json(), expected_response)

    def test_update_user(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)
        response = self.client.put(reverse('profilemodel-detail', args=[profile.pk,]), self.new_data)
        expected_response = {'pk': 1, 'url': 'http://testserver/api/users/1/', 'country': None,
                             'phone': '800555359000', 'birthdate': None, 'short_status': 'Короткий статус',
                             'first_name': 'Аноним', 'linkedin': '', 'last_name': 'Аноним'}
        self.assertEqual(response.json(), expected_response)

    def test_destroy_user(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)
        response = self.client.delete(reverse('profilemodel-detail', args=[profile.pk,]))
        self.assertEqual(response.status_code, 204)

    def test_add_friend(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)
        friend = self.register_user(self.second_user_data)
        profile_friend = ProfileModel.objects.get(user=friend.json().get('id'))
        response = self.client.post(reverse('profilemodel-add-friend', args=[profile.pk,]),
                                    {'friend_pk': profile_friend.pk})
        self.assertEqual(response.json(), {'status': True})

    def test_get_friends(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)
        friend = self.register_user(self.second_user_data)
        profile_friend = ProfileModel.objects.get(user=friend.json().get('id'))
        self.client.post(reverse('profilemodel-add-friend', args=[profile.pk,]), {'friend_pk': profile_friend.pk})
        response = self.client.get(reverse('profilemodel-get-friends', args=[profile.pk,]))
        excepted_response = [{'url': 'http://testserver/api/users/2/', 'country': None, 'last_name': 'Аноним',
                              'first_name': 'Аноним', 'birthdate': None, 'short_status': '',
                              'pk': 2, 'linkedin': '', 'phone': '8005553593'}]
        self.assertEqual(response.json(), excepted_response)

    def test_remove_friend(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)
        friend = self.register_user(self.second_user_data)
        profile_friend = ProfileModel.objects.get(user=friend.json().get('id'))
        response = self.client.post(reverse('profilemodel-remove-friend', args=[profile.pk,]),
                                    {'friend_pk': profile_friend.pk})
        self.assertEqual(response.json(), {'status': True})

    def test_permission_checking(self):
        user = self.register_user(self.first_user_data)
        profile = ProfileModel.objects.get(user=user.json().get('id'))
        response = self.client.delete(reverse('profilemodel-detail', args=[profile.pk,]))
        excepted_response = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.json(), excepted_response)

    def register_user(self, data):
        response = self.client.post(reverse('profilemodel-list'), data)
        return response

    def register_user_with_auth(self):
        register_response = self.register_user(self.first_user_data)
        response_json = register_response.json()
        user = User.objects.get(pk=response_json.get('id'))
        self.client.force_login(user=user)
        return user
