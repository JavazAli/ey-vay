from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [

    # فیلم‌ها
    path("", views.movie_list, name="movie_list"),
    path("add/", views.movie_create, name="movie_add"),
    path("edit/<int:pk>/", views.movie_update, name="movie_edit"),
    path("delete/<int:pk>/", views.movie_delete, name="movie_delete"),

    # اکران‌ها
    path("screenings/", views.screening_list, name="screening_list"),
    path("screenings/add/", views.screening_create, name="screening_add"),
    path("screenings/<int:pk>/edit/", views.screening_update, name="screening_update"),
    path("screenings/<int:pk>/delete/", views.screening_delete, name="screening_delete"),
    path("ajax/load-showtimes/", views.load_showtimes, name="ajax_load_showtimes"),
]
