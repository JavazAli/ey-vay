from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # صفحه اصلی و ورود
    path('', views.home_view, name='home'),
    
    # ثبت‌نام
    path('signup/', views.signup_view, name='signup'),
    
    # پنل ادمین
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # خروج
    path('logout/', views.logout_view, name='logout'),
    path("customer/home/", views.customer_home, name="customer_home"),
    path("customer/wallet/", views.wallet_view, name="wallet"),

    #صفحه سینما ها برای مشتری
    path("customer/cinemas/", views.customer_cinema_list, name="customer_cinema_list"),

    # صفحه لیست فیلم‌های یک سینما
    path("customer/cinemas/<int:cinema_id>/movies/",views.customer_movie_list,name="customer_movie_list"),
    path(
        "customer/cinemas/<int:cinema_id>/movies/<int:movie_id>/",
        views.customer_movie_detail,
        name="customer_movie_detail",
    ),

]
