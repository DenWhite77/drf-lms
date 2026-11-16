from django.core.management.base import BaseCommand
from users.models import CustomUser, Payment
from lms.models import Course, Lesson
from decimal import Decimal


class Command(BaseCommand):
    help = 'Создает тестовые данные: курсы, уроки и платежи'

    def handle(self, *args, **kwargs):
        # 1. Создаем пользователя (если нет)
        user, created = CustomUser.objects.get_or_create(
            email='student@drf-lms.local',
            defaults={'city': 'Москва', 'phone': '+79990000000'}
        )
        if created:
            user.set_password('student123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Создан пользователь student@drf-lms.local'))

        # 2. Создаем курсы
        course1, _ = Course.objects.get_or_create(title='Python для начинающих', defaults={'description': 'Базовый курс'})
        course2, _ = Course.objects.get_or_create(title='Django REST Framework', defaults={'description': 'Продвинутый курс'})

        # 3. Создаем уроки
        lesson1, _ = Lesson.objects.get_or_create(course=course1, title='Введение в Python', defaults={'video_link': 'https://youtube.com/1'})
        lesson2, _ = Lesson.objects.get_or_create(course=course1, title='Установка Python', defaults={'video_link': 'https://youtube.com/2'})
        lesson3, _ = Lesson.objects.get_or_create(course=course2, title='Основы DRF', defaults={'video_link': 'https://youtube.com/3'})

        # 4. Создаем платежи
        Payment.objects.get_or_create(user=user, course=course1, amount=Decimal('5000.00'), payment_method='transfer')
        Payment.objects.get_or_create(user=user, course=course2, amount=Decimal('7000.00'), payment_method='cash')
        Payment.objects.get_or_create(user=user, lesson=lesson1, amount=Decimal('1000.00'), payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
