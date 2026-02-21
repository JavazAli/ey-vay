from django import forms


class ReservationForm(forms.Form):
    PAYMENT_METHOD_CHOICES = (
        ("normal", "پرداخت عادی"),
        ("wallet", "پرداخت از طریق کیف پول"),
    )

    seats = forms.IntegerField(
        min_value=1,
        initial=1,
        label="تعداد صندلی",
        error_messages={
            "min_value": "تعداد صندلی باید حداقل ۱ باشد.",
            "invalid": "تعداد صندلی معتبر نیست.",
        },
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        initial="normal",
        label="روش پرداخت",
    )
