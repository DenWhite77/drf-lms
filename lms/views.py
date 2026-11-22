from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal
from drf_spectacular.utils import extend_schema

from .models import Course, Lesson, Subscription
from users.models import Payment
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner, IsOwnerAndNotModerator, IsModeratorOrOwner
from .paginators import StandardResultsSetPagination

# Импорты из твоего нового файла services.py
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    get_stripe_session_status,
)

# --- Курсы (ViewSet) ---
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerAndNotModerator]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        from .tasks import send_course_update_email
        send_course_update_email.delay(instance.id)


# --- Уроки (Generic) ---
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), IsModeratorOrOwner()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsOwnerAndNotModerator()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        from django.utils import timezone
        from datetime import timedelta
        from .tasks import send_course_update_email

        instance = serializer.save()
        course = instance.course


        if course.updated_at < timezone.now() - timedelta(hours=4):
            course.save()
            send_course_update_email.delay(course.id)


class SubscriptionAPIView(APIView):
    """Подписка / отписка от обновлений курса."""

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


@extend_schema(
    summary="Создание платежа",
    description="Создает продукт и цену в Stripe, возвращает ссылку на оплату.",
    request={"application/json": {"type": "object", "properties": {"course_id": {"type": "integer"}, "lesson_id": {"type": "integer"}}}}, # <--- ДОБАВИТЬ ЭТО
    responses={201: None}
)
class PaymentCreateAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if course_id:
            item = get_object_or_404(Course, id=course_id)
            amount = Decimal('1000.00')  # Заглушка суммы
            item_name = item.title
        elif lesson_id:
            item = get_object_or_404(Lesson, id=lesson_id)
            amount = Decimal('500.00')  # Заглушка суммы
            item_name = item.title
        else:
            return Response({"error": "Укажите course_id или lesson_id"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Создаем продукт
        product_id = create_stripe_product(item_name)

        # 2. Создаем цену (в копейках!)
        amount_kopecks = int(amount * 100)
        price_id = create_stripe_price(product_id, amount_kopecks)

        # 3. Создаем сессию
        success_url = "http://127.0.0.1:8000/api/payments/success/"
        cancel_url = "http://127.0.0.1:8000/api/payments/cancel/"
        session = create_stripe_session(price_id, success_url, cancel_url)

        # 4. Сохраняем в базу
        payment = Payment.objects.create(
            user=user,
            course=item if course_id else None,
            lesson=item if lesson_id else None,
            amount=amount,
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_id=session.id,
            payment_link=session.url,
            status='pending'
        )

        return Response({
            "payment_link": payment.payment_link,
            "payment_id": payment.id
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Статус платежа",
    description="Возвращает статус сессии оплаты по её ID.",
)
class PaymentStatusAPIView(APIView):
    def get(self, request, session_id):
        status_stripe = get_stripe_session_status(session_id)
        return Response({"status": status_stripe})
