from django.test import TestCase
from django.urls import reverse


class APITestCase(TestCase):
    def test_courses_api_status(self):
        # Проверяем, что API курсов доступно (возвращает 200)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
