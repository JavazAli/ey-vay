from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from cinemas.models import Cinema, ShowTime
from movies.models import Movie, Screening


class CustomerMovieDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer1",
            password="testpass123",
            phone_number="09120000001",
            role="customer",
        )

        self.cinema = Cinema.objects.create(name="Cinema A", capacity=100)
        self.showtime = ShowTime.objects.create(date="2026-01-10", start_time="18:00")
        self.movie = Movie.objects.create(
            title="Movie A",
            genre="Drama",
            director="Director A",
            actors="Actor 1, Actor 2",
            summary="Sample summary",
            year=2025,
        )
        self.screening = Screening.objects.create(
            cinema=self.cinema,
            showtime=self.showtime,
            movie=self.movie,
            remaining_seats=42,
        )

    def test_customer_movie_detail_requires_login(self):
        url = reverse(
            "accounts:customer_movie_detail",
            kwargs={"cinema_id": self.cinema.id, "movie_id": self.movie.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:home"))

    def test_customer_movie_detail_shows_movie_and_showtimes(self):
        self.client.login(username="customer1", password="testpass123")
        url = reverse(
            "accounts:customer_movie_detail",
            kwargs={"cinema_id": self.cinema.id, "movie_id": self.movie.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)
        self.assertContains(response, self.cinema.name)
        self.assertContains(response, "42")
        self.assertContains(response, "18:00")

    def test_customer_movie_detail_selected_screening_in_context(self):
        self.client.login(username="customer1", password="testpass123")
        url = reverse(
            "accounts:customer_movie_detail",
            kwargs={"cinema_id": self.cinema.id, "movie_id": self.movie.id},
        )

        response = self.client.get(url, {"screening": self.screening.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_screening"], self.screening)