from django import forms
from .models import Movie , Screening

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'summary', 'genre', 'director', 'actors']
        labels = {
            'title': 'عنوان فیلم',
            'summary': 'خلاصه داستان',
            'genre': 'ژانر',
            'director': 'کارگردان',
            'actors': 'بازیگران اصلی',
        }
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
            "actors": forms.Textarea(attrs={"rows": 3}),
        }


from django import forms
from .models import Screening

class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = [
            'cinema',
            'movie',
            'showtime',
            'remaining_seats'
        ]
        labels = {
            'cinema': 'سینما',
            'movie': 'فیلم',
            'showtime': 'سانس',
            'remaining_seats': 'ظرفیت اولیه',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اجازه بده فرم این فیلد خالی باشد
        self.fields['remaining_seats'].required = False

    def clean(self):
        cleaned_data = super().clean()
        cinema = cleaned_data.get("cinema")
        movie = cleaned_data.get("movie")
        showtime = cleaned_data.get("showtime")
        remaining_seats = cleaned_data.get("remaining_seats")

        # جلوگیری از ثبت تکراری
        if Screening.objects.filter(
            cinema=cinema,
            movie=movie,
            showtime=showtime
        ).exists():
            raise forms.ValidationError(
                "این اکران قبلاً ثبت شده است."
            )

        # اگر کاربر ظرفیت وارد نکرده بود، از ظرفیت سالن استفاده کن
        if remaining_seats is None and cinema is not None:
            cleaned_data['remaining_seats'] = cinema.capacity

        return cleaned_data
