from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription


@shared_task
def send_course_update_email(course_id):
    # Находим всех подписчиков этого курса
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user', 'course')

    for sub in subscriptions:
        subject = f"Обновление курса: {sub.course.title}"
        message = f"Здравствуйте! В курсе '{sub.course.title}' появились новые материалы. Зайдите и проверьте!"
        email_from = settings.EMAIL_HOST_USER or 'noreply@example.com'
        send_mail(subject, message, email_from, [sub.user.email])

    return f"Отправлено писем: {subscriptions.count()}"
