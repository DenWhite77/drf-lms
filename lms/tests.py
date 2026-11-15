from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from lms.models import Course

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        # Создаем клиент DRF
        self.client = APIClient()
        # Получаем JWT токен для этого пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        # Добавляем токен в заголовки авторизации
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_courses_api_status_authorized(self):
        # Проверяем, что авторизованный пользователь получает 200
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)

    def test_courses_api_status_unauthorized(self):
        # Проверяем, что без токена возвращается 401
        unauthorized_client = APIClient()
        response = unauthorized_client.get('/api/courses/')
        self.assertEqual(response.status_code, 401)
