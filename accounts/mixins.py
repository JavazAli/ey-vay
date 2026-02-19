from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin برای Class-Based Views که فقط به ادمین‌ها دسترسی می‌دهد
    """
    
    def test_func(self):
        """
        تست می‌کند که آیا کاربر ادمین است یا نه
        """
        return self.request.user.is_authenticated and self.request.user.role == 'admin'
    
    def handle_no_permission(self):
        """
        اگر کاربر دسترسی نداشته باشد چه اتفاقی بیفتد
        """
        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'لطفاً ابتدا وارد شوید.')
            return redirect('accounts:home')
        else:
            messages.error(self.request, 'شما به این بخش دسترسی ندارید.')
            return redirect('accounts:customer_home')
