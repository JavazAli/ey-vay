from django.db import models
from cinemas.models import Cinema
from cinemas.models import ShowTime


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    actors = models.TextField()
    summary = models.TextField(blank=True, null=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class Screening(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    remaining_seats = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cinema', 'movie', 'showtime')

    def __str__(self):
        return f"{self.movie} at {self.cinema} on {self.showtime}"
