from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from accounts.decorators import login_required_custom
from movies.models import Screening

from .factories import ReservationFactory
from .forms import ReservationForm
from .models import Reservation


@login_required_custom
@require_http_methods(["POST"])
def create_reservation(request, screening_id):
    form = ReservationForm(request.POST)
    screening_for_view = get_object_or_404(
        Screening.objects.select_related("movie", "cinema", "showtime"),
        id=screening_id,
    )

    if not form.is_valid():
        return render(
            request,
            "reservations/reservation_result.html",
            {
                "success": False,
                "error_message": "ورودی رزرو نامعتبر است.",
                "screening": screening_for_view,
                "seats": request.POST.get("seats", 1),
            },
        )

    seats = form.cleaned_data["seats"]

    with transaction.atomic():
        screening = (
            Screening.objects.select_for_update()
            .select_related("movie", "cinema", "showtime")
            .get(id=screening_id)
        )

        if screening.remaining_seats < seats:
            return render(
                request,
                "reservations/reservation_result.html",
                {
                    "success": False,
                    "error_message": "ظرفیت کافی برای رزرو وجود ندارد.",
                    "screening": screening,
                    "seats": seats,
                },
            )

        screening.remaining_seats -= seats
        screening.save(update_fields=["remaining_seats"])

        reservation = ReservationFactory.create(
            user=request.user,
            screening=screening,
            seats=seats,
        )

    return render(
        request,
        "reservations/reservation_result.html",
        {
            "success": True,
            "reservation": reservation,
            "screening": reservation.screening,
        },
    )


@login_required_custom
def reservation_result(request, code):
    reservation = get_object_or_404(
        Reservation.objects.select_related("screening__movie", "screening__cinema", "screening__showtime"),
        code=code,
        user=request.user,
    )
    return render(
        request,
        "reservations/reservation_result.html",
        {
            "success": True,
            "reservation": reservation,
            "screening": reservation.screening,
        },
    )
