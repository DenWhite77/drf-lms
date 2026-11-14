from rest_framework import generics, viewsets
from .models import CustomUser, Payment
from .serializers import UserSerializer, PaymentSerializer
from .filters import PaymentFilter


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка платежей с фильтрацией и сортировкой."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # по умолчанию: новые сверху
