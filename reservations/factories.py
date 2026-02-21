import secrets

from .models import Reservation


class ReservationFactory:
    """Factory برای ساخت رزرو و تولید کد پیگیری یکتا."""

    @staticmethod
    def _generate_tracking_code(length=10):
        return secrets.token_hex(length // 2).upper()[:length]

    @classmethod
    def create(cls, *, user, screening, seats):
        while True:
            code = cls._generate_tracking_code()
            if not Reservation.objects.filter(code=code).exists():
                break

        return Reservation.objects.create(
            user=user,
            screening=screening,
            seats=seats,
            code=code,
        )