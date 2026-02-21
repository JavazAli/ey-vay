from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cinemas.models import Cinema, ShowTime
from movies.models import Movie, Screening
from reservations.models import Reservation


class ReservationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer1",
            password="testpass123",
            phone_number="09120000001",
            role="customer",
        )
        self.cinema = Cinema.objects.create(name="ایران", capacity=10)
        self.showtime = ShowTime.objects.create(date=date(2026, 1, 1), start_time=time(18, 0))
        self.movie = Movie.objects.create(
            title="Movie A",
            genre="Drama",
            director="Director",
            actors="Actor 1, Actor 2",
            summary="Summary",
        )
        self.screening = Screening.objects.create(
            cinema=self.cinema,
            movie=self.movie,
            showtime=self.showtime,
            remaining_seats=5,
        )

        self.client.login(username="customer1", password="testpass123")

    def test_reservation_success_decreases_capacity(self):
        response = self.client.post(
            reverse("reservations:create_reservation", args=[self.screening.id]),
            {"seats": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "رزرو با موفقیت انجام شد")

        self.screening.refresh_from_db()
        self.assertEqual(self.screening.remaining_seats, 3)

        reservation = Reservation.objects.get(screening=self.screening, user=self.user)
        self.assertEqual(reservation.seats, 2)
        self.assertTrue(reservation.code)

    def test_reservation_fails_when_capacity_insufficient(self):
        response = self.client.post(
            reverse("reservations:create_reservation", args=[self.screening.id]),
            {"seats": 6},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ظرفیت کافی برای رزرو وجود ندارد")

        self.screening.refresh_from_db()
        self.assertEqual(self.screening.remaining_seats, 5)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_code_page(self):
        reservation = Reservation.objects.create(
            user=self.user,
            screening=self.screening,
            seats=1,
            code="ABC1234567",
        )

        response = self.client.get(
            reverse("reservations:reservation_result", args=[reservation.code])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC1234567")
