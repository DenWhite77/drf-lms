from rest_framework import generics, viewsets, permissions
from .models import CustomUser, Payment
from .serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from .filters import PaymentFilter
from .permissions import IsSelf


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Вместо | используем список, который понимает и Django, и Swagger
        class IsAdminOrSelf(permissions.BasePermission):
            def has_object_permission(self, request, view, obj):
                return request.user.is_staff or request.user == obj

            def has_permission(self, request, view):
                return request.user and request.user.is_authenticated

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSelf()]
        return [permissions.IsAuthenticated()]


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
