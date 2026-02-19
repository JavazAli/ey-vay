from django.urls import path
from . import views

urlpatterns = [
    path("cinemas/", views.cinema_list, name="cinema_list"),
    path("cinemas/create/", views.cinema_create, name="cinema_create"),
    path("cinemas/<int:pk>/edit/", views.cinema_update, name="cinema_update"),
    path("cinemas/<int:pk>/delete/", views.cinema_delete, name="cinema_delete"),
    path("showtimes/", views.showtime_list, name="showtime_list"),
    path("showtimes/create/", views.showtime_create, name="showtime_create"),
    path("showtimes/<int:pk>/edit/", views.showtime_update, name="showtime_update"),
    path("showtimes/<int:pk>/delete/", views.showtime_delete, name="showtime_delete"),

]
