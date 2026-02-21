from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Movie, Screening
from .forms import MovieForm, ScreeningForm

from cinemas.models import Cinema
from accounts.decorators import admin_required


# =========================================================
# مدیریت فیلم‌ها
# =========================================================

@admin_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies/movie_list.html", {"movies": movies})


@admin_required
def movie_create(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "فیلم با موفقیت اضافه شد.")
            return redirect("movies:movie_list")
        else:
            messages.error(request, "خطا در ثبت فیلم. لطفاً مقادیر را بررسی کنید.")

    return render(request, "movies/movie_form.html", {"form": form})


@admin_required
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.POST or None, instance=movie)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "فیلم با موفقیت ویرایش شد.")
            return redirect("movies:movie_list")
        else:
            messages.error(request, "خطا در ویرایش فیلم.")

    return render(request, "movies/movie_form.html", {"form": form, "movie": movie})


@admin_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        movie.delete()
        messages.success(request, "فیلم با موفقیت حذف شد.")
        return redirect("movies:movie_list")

    return render(request, "movies/movie_confirm_delete.html", {"movie": movie})


# =========================================================
# مدیریت اکران‌ها
# =========================================================

@admin_required
def screening_list(request):
    screenings = Screening.objects.select_related(
        "movie", "cinema", "showtime"
    )
    return render(
        request,
        "movies/screening_list.html",
        {"screenings": screenings}
    )


@admin_required
def screening_create(request):
    form = ScreeningForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            screening = form.save(commit=False)

            # اگر ظرفیت وارد نشده باشد از ظرفیت سینما استفاده کن
            if not screening.remaining_seats:
                screening.remaining_seats = screening.cinema.capacity

            screening.save()
            messages.success(request, "اکران با موفقیت ثبت شد.")
            return redirect("movies:screening_list")
        else:
            messages.error(request, "خطا در ثبت اکران. مقادیر را بررسی کنید.")

    return render(request, "movies/screening_form.html", {"form": form})


@admin_required
def screening_update(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    form = ScreeningForm(request.POST or None, instance=screening)

    if request.method == "POST":
        if form.is_valid():
            screening = form.save(commit=False)

            if not screening.remaining_seats:
                screening.remaining_seats = screening.cinema.capacity

            screening.save()
            messages.success(request, "اکران با موفقیت ویرایش شد.")
            return redirect("movies:screening_list")
        else:
            messages.error(request, "خطا در ویرایش اکران.")

    return render(
        request,
        "movies/screening_form.html",
        {"form": form, "screening": screening}
    )


@admin_required
def screening_delete(request, pk):
    screening = get_object_or_404(Screening, pk=pk)

    if request.method == "POST":
        screening.delete()
        messages.success(request, "اکران با موفقیت حذف شد.")
        return redirect("movies:screening_list")

    return render(
        request,
        "movies/screening_confirm_delete.html",
        {"screening": screening}
    )


# =========================================================
# Ajax – فیلتر سانس‌ها بر اساس سینما
# =========================================================

@admin_required
def load_showtimes(request):
    cinema_id = request.GET.get("cinema")

    showtimes = []

    if cinema_id:
        try:
            cinema = Cinema.objects.get(id=cinema_id)
            showtimes = cinema.showtimes.all()
        except Cinema.DoesNotExist:
            showtimes = []

    data = [
        {
            "id": show.id,
            "text": str(show)
        }
        for show in showtimes
    ]

    return JsonResponse(data, safe=False)