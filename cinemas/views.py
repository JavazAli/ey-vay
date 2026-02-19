from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cinema
from .forms import CinemaForm
from .models import ShowTime 
from .forms import ShowTimeForm
from accounts.decorators import admin_required

@admin_required
def cinema_list(request):
    cinemas = Cinema.objects.all()
    return render(request, "cinemas/cinema_list.html", {"cinemas": cinemas})

@admin_required
def cinema_create(request):
    if request.method == "POST":
        form = CinemaForm(request.POST)
        if form.is_valid():
            cinema = form.save(commit=False)
            cinema.save()
            form.save_m2m()
            messages.success(request, " سینما با موفقیت ایجاد شد.")
            return redirect("cinema_list")
    else:
        form = CinemaForm()
    return render(request, "cinemas/cinema_form.html", {"form": form, "title": "ایجاد سینما"})

@admin_required
def cinema_update(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == "POST":
        form = CinemaForm(request.POST, instance=cinema)
        if form.is_valid():
            cinema = form.save(commit=False)
            cinema.save()
            form.save_m2m()
            messages.info(request, "سینما با موفقیت ویرایش شد.")
            return redirect("cinema_list")
    else:
        form = CinemaForm(instance=cinema)
    return render(request, "cinemas/cinema_form.html", {"form": form, "title": "ویرایش سینما"})

@admin_required
def cinema_delete(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == "POST":
        cinema.delete()
        messages.error(request, "سینما با موفقیت حذف شد.")
        return redirect("cinema_list")
    return render(request, "cinemas/cinema_confirm_delete.html", {"cinema": cinema})



@admin_required
def showtime_list(request):
    showtimes = ShowTime.objects.all()
    return render(request, "cinemas/showtime_list.html", {"showtimes": showtimes})

@admin_required
def showtime_create(request):
    if request.method == "POST":
        form = ShowTimeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " سانس با موفقیت ایجاد شد.")
            return redirect("showtime_list")
    else:
        form = ShowTimeForm()
    return render(request, "cinemas/showtime_form.html", {"form": form, "title": "ایجاد سانس"})

@admin_required
def showtime_update(request, pk):
    showtime = get_object_or_404(ShowTime, pk=pk)
    if request.method == "POST":
        form = ShowTimeForm(request.POST, instance=showtime)
        if form.is_valid():
            form.save()
            messages.info(request, " سانس با موفقیت ویرایش شد.")
            return redirect("showtime_list")
    else:
        form = ShowTimeForm(instance=showtime)
    return render(request, "cinemas/showtime_form.html", {"form": form, "title": "ویرایش سانس"})

@admin_required
def showtime_delete(request, pk):
    showtime = get_object_or_404(ShowTime, pk=pk)
    if request.method == "POST":
        showtime.delete()
        messages.error(request, " سانس با موفقیت حذف شد.")
        return redirect("showtime_list")
    return render(request, "cinemas/showtime_confirm_delete.html", {"showtime": showtime})




def customer_home(request):
    query = request.GET.get("q", "").strip()
    cinemas = Cinema.objects.all()
    if query:
        cinemas = cinemas.filter(name__icontains=query)

    context = {
        "cinemas": cinemas,
        "query": query,
    }
    return render(request, "accounts/customer_home.html", context)
