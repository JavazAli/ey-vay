from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("screenings/<int:screening_id>/create/", views.create_reservation, name="create_reservation"),
    path("result/<str:code>/", views.reservation_result, name="reservation_result"),
]
