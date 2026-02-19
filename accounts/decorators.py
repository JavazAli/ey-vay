from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """
    Decorator برای چک کردن اینکه کاربر ادمین است یا نه
    اگر کاربر لاگین نکرده باشد، به صفحه لاگین هدایت می‌شود
    اگر کاربر مشتری باشد، پیام خطا نمایش داده و به صفحه اصلی هدایت می‌شود
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # چک کردن لاگین بودن کاربر
        if not request.user.is_authenticated:
            messages.warning(request, 'لطفاً ابتدا وارد شوید.')
            return redirect('accounts:home')
        
        # چک کردن ادمین بودن کاربر با استفاده از فیلد role
        if request.user.role != "admin":
            messages.error(request, 'شما به این بخش دسترسی ندارید.')
            return redirect('accounts:customer_home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

# accounts/decorators.py
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "لطفاً ابتدا وارد شوید.")
            return redirect("accounts:home")  # چون app_name = 'accounts' داری
        return view_func(request, *args, **kwargs)
    return wrapper
