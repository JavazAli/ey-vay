from django.db import models

class ShowTime(models.Model):
    date = models.DateField()
    start_time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start_time}"


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    showtimes = models.ManyToManyField(ShowTime, blank=True, related_name="cinemas")

    def __str__(self):
        return self.name
