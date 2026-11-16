import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    # Фильтр по точному ID курса
    course = django_filters.NumberFilter(field_name='course__id')
    # Фильтр по точному ID урока
    lesson = django_filters.NumberFilter(field_name='lesson__id')
    # Фильтр по способу оплаты
    payment_method = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
