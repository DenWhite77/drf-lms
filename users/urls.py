from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRetrieveUpdateAPIView, PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
]
