from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Movie, Screening
from .forms import MovieForm, ScreeningForm

from accounts.decorators import admin_required


# =========================================================
# مدیریت فیلم‌ها
# =========================================================

# -----------------------------
# لیست فیلم‌ها
# -----------------------------
@admin_required
def movie_list(request):
    movies = Movie.objects.all()

    return render(
        request,
        "movies/movie_list.html",
        {"movies": movies}
    )


# -----------------------------
# افزودن فیلم
# -----------------------------
@admin_required
def movie_create(request):

    form = MovieForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "فیلم با موفقیت اضافه شد.")
            return redirect("movies:movie_list")
        else:
            messages.error(
                request,
                "خطا در ثبت فیلم. لطفاً مقادیر را بررسی کنید."
            )

    return render(
        request,
        "movies/movie_form.html",
        {"form": form}
    )


# -----------------------------
# ویرایش فیلم
# -----------------------------
@admin_required
def movie_update(request, pk):

    movie = get_object_or_404(Movie, pk=pk)

    form = MovieForm(
        request.POST or None,
        instance=movie
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "فیلم با موفقیت ویرایش شد."
            )
            return redirect("movies:movie_list")
        else:
            messages.error(
                request,
                "خطا در ویرایش فیلم."
            )

    return render(
        request,
        "movies/movie_form.html",
        {
            "form": form,
            "movie": movie
        }
    )


# -----------------------------
# حذف فیلم
# -----------------------------
@admin_required
def movie_delete(request, pk):

    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        movie.delete()
        messages.success(
            request,
            "فیلم با موفقیت حذف شد."
        )
        return redirect("movies:movie_list")

    return render(
        request,
        "movies/movie_confirm_delete.html",
        {"movie": movie}
    )


# =========================================================
#  مدیریت اکران‌ها (Screening)
# =========================================================

# -----------------------------
# لیست اکران‌ها
# -----------------------------
@admin_required
def screening_list(request):

    screenings = Screening.objects.select_related(
        "movie",
        "cinema",
        "showtime"
    )

    return render(
        request,
        "movies/screening_list.html",
        {"screenings": screenings}
    )


# -----------------------------
# افزودن اکران
# -----------------------------

@admin_required
def screening_create(request):
    form = ScreeningForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            screening = form.save(commit=False)

            # ظرفیت را از سالن انتخاب شده بگیریم
            screening.remaining_seats = screening.cinema.capacity

            screening.save()
            messages.success(request, "اکران با موفقیت ثبت شد.")
            return redirect("movies:screening_list")

        else:
            messages.error(request, "این ترکیب فیلم، سینما و سانس قبلاً ثبت شده است.")

    return render(request, "movies/screening_form.html", {"form": form})
