from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Payment


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Убираем стандартные поля, которых нет в CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('phone', 'city', 'avatar')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_active')
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_date', 'amount', 'payment_method', 'course', 'lesson')
    list_filter = ('payment_method', 'course', 'lesson')
