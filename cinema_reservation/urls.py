from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # صفحه اصلی
    path('', accounts_views.home_view, name='home'),
    path('signup/', accounts_views.signup_view, name='signup'),
    
    # Accounts URLs
    path('accounts/', include('accounts.urls')),
    
    # Cinemas URLs
    path('cinemas/', include('cinemas.urls')),
    
    # Movies URLs
    path('movies/', include('movies.urls')),
    
    # Reservations URLs
    path('reservations/', include('reservations.urls')),
]
