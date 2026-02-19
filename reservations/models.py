from django.utils import timezone
from django.db import models
from movies.models import Screening

class Reservation(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    code = models.CharField(max_length=20, unique=True)
    reserved_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation {self.code} for {self.user}"
