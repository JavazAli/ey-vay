from django import forms
from .models import Cinema, ShowTime

class CinemaForm(forms.ModelForm):
    showtimes = forms.ModelMultipleChoiceField(
        queryset=ShowTime.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="showtimes:"
    )

    class Meta:
        model = Cinema
        fields = ["name", "capacity", "showtimes"]


class ShowTimeForm(forms.ModelForm):
    class Meta:
        model = ShowTime
        fields = ["date", "start_time"]
        widgets = { "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}), "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}), }