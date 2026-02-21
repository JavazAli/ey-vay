from django import forms
from .models import Movie, Screening, ShowTime

# =========================
# فرم فیلم
# =========================
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

# =========================
# فرم اکران
# =========================
from django import forms
from .models import Screening
from cinemas.models import ShowTime


class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # در ابتدا هیچ سانسی نمایش داده نشود
        self.fields["showtime"].queryset = ShowTime.objects.none()

        # اگر فرم POST شده باشد
        if "cinema" in self.data and "movie" in self.data:
            try:
                cinema_id = int(self.data.get("cinema"))
                movie_id = int(self.data.get("movie"))

                self.fields["showtime"].queryset = ShowTime.objects.filter(
                    cinema_id=cinema_id
                )

            except (ValueError, TypeError):
                pass

        # هنگام ویرایش
        elif self.instance.pk:
            self.fields["showtime"].queryset = ShowTime.objects.filter(
                cinema=self.instance.cinema
            )