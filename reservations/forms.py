from django import forms


class ReservationForm(forms.Form):
    seats = forms.IntegerField(
        min_value=1,
        initial=1,
        label="تعداد صندلی",
        error_messages={
            "min_value": "تعداد صندلی باید حداقل ۱ باشد.",
            "invalid": "تعداد صندلی معتبر نیست.",
        },
    )