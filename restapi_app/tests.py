from rest_framework.test import APITestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User

from profiles_app.models import ProfileModel


class APIListViewTest(APITestCase):
    first_user_data = {'password': 'MyPass2018', 'username': 'admin2', 'phone': '80055535943'}
    second_user_data = {'password': 'MyPass2018', 'username': 'admin3', 'phone': '8005553593'}

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

        new_data = {'short_status': 'Короткий статус', 'phone': '800555359000'}
        response = self.client.put(reverse('profilemodel-detail', args=[profile.pk,]), new_data)
        expected_response = {'pk': 1, 'url': 'http://testserver/api/users/1/', 'country': None,
                             'phone': '800555359000', 'birthdate': None, 'short_status': 'Короткий статус',
                             'first_name': 'Аноним', 'linkedin': '', 'last_name': 'Аноним'}
        self.assertEqual(response.json(), expected_response)

    def test_destroy_user(self):
        user = self.register_user_with_auth()
        profile = ProfileModel.objects.get(user=user)

        response = self.client.delete(reverse('profilemodel-detail', args=[profile.pk,]))
        self.assertEqual(response.status_code, 204)

    def register_user(self, data):
        response = self.client.post(reverse('profilemodel-list'), data)
        return response

    # Для последующих запросов, требующих авторизации пользователя
    def register_user_with_auth(self):
        register_response = self.register_user(self.first_user_data)
        response_json = register_response.json()
        pk = response_json.get('id')
        user = User.objects.get(pk=pk)
        self.client.force_login(user=user)
        return user
    # Получить список друзей
    # Отправить/отозвать заявку в друзья
    # Проверка требования токенов на соответствующих запросах
