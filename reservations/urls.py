from django.urls import path
from django.shortcuts import redirect

app_name = 'reservations'

def go_to_screening_list(request):
    # این URL رو به view واقعی movies هدایت می‌کنه
    return redirect('movies:screening_list')

urlpatterns = [
    path('screenings/', go_to_screening_list, name='screening_list'),
]
