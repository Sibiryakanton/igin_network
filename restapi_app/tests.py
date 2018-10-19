from rest_framework.test import APITestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User


class APIListViewTest(APITestCase):
    first_user_data ={'password': 'MyPass2018', 'username': 'admin2', 'phone': '80055535943'}
    second_user_data ={'password': 'MyPass2018', 'username': 'admin3', 'phone': '8005553593'}

    client = Client()

    def test_get_token(self):
        self.test_register_user()
        data = {'password': 'MyPass2018', 'username': 'admin2'}
        response = self.client.post(reverse('get_token'), data)
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        data = {'password': 'MyPass2018', 'username': 'admin2', 'phone': '80055535943',}
        response = self.client.post(reverse('profilemodel-list'), data)
        expected_response = {'id': 1}
        self.assertEqual(response.json(), expected_response)

    # Для последующих запросов, требующих авторизации пользователя
    def register_user_with_auth(self):
        self.test_register_user()
        username = self.first_user_data.get('username')
        user = User.objects.get(username=username)
        self.client.force_login(user=user)

    # Получить список друзей
    # Отправить/отозвать заявку в друзья
    # Обновить профиль
    # Удалить профиль
    # Проверка требования токенов на соответствующих запросах
