from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from lms.models import Course, Lesson, Subscription

User = get_user_model()


class LessonTestCase(TestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.local', password='test123')
        self.moderator = User.objects.create_user(email='moder@test.local', password='test123')
        self.other_user = User.objects.create_user(email='other@test.local', password='test123')

        # Назначаем модератора в группу (пока просто создадим, если нужно)
        # from django.contrib.auth.models import Group
        # group, _ = Group.objects.get_or_create(name='Модераторы')
        # self.moderator.groups.add(group)

        # Создаем курс и урок
        self.course = Course.objects.create(title='Тестовый курс', owner=self.user)
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            course=self.course,
            video_link='https://youtube.com/watch?v=123',
            owner=self.user
        )

        self.client = APIClient()

    # --- Тесты CRUD уроков ---

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_link': 'https://youtube.com/watch?v=456'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_lesson_create_invalid_youtube_link(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_link': 'https://vimeo.com/watch?v=456'  # Сторонняя ссылка
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_lesson_update_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Обновленный урок'}
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')

    def test_lesson_delete_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    # --- Тесты прав доступа ---

    def test_lesson_update_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Хакерский взлом'}
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_unauthorized(self):
        # Без токена
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='sub@test.local', password='test123')
        self.course = Course.objects.create(title='Курс для подписки', owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscription_add(self):
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscriptions/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_remove(self):
        # Сначала подписываемся
        Subscription.objects.create(user=self.user, course=self.course)

        # Потом отписываемся
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscriptions/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
