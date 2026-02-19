from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Wallet


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    پنل ادمین برای مدل User
    """
    list_display = ('username', 'phone_number', 'role', 'first_name', 'last_name', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number', 'first_name', 'last_name')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone_number', 'role')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone_number', 'role')}),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مدل Wallet
    """
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__phone_number')
    list_filter = ('balance',)
