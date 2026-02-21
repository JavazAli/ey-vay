from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import PhoneLoginForm, SignupForm, WalletTopUpForm
from .models import User, Wallet
from .decorators import admin_required
from .mixins import AdminRequiredMixin
from .decorators import login_required_custom 
from cinemas.models import Cinema
from movies.models import Movie, Screening

def home_view(request):
    """
    صفحه اصلی: ورود با شماره تلفن + رمز عبور
    """
    show_password = False  # ابتدا فقط شماره نمایش داده می‌شود

    if request.method == "POST":
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            password = form.cleaned_data.get("password")
            user = User.objects.filter(phone_number=phone).first()

            if user:
                show_password = True  # شماره موجوده → فیلد رمز نمایش داده می‌شود
                if password:  # اگر رمز هم وارد شده
                    if user.check_password(password):
                        login(request, user)
                        messages.success(request, "ورود موفقیت‌آمیز بود!")
                        if user.role == "admin":
                            return redirect("accounts:admin_panel")
                        else:
                            return redirect("accounts:customer_home")
                    else:
                        messages.error(request, "رمز عبور اشتباه است!")
            else:
                messages.info(request, "کاربری با این شماره یافت نشد. لطفاً ثبت‌نام کنید.")
                return redirect("signup")  # شماره وجود ندارد → ثبت‌نام
    else:
        form = PhoneLoginForm()

    return render(
        request,
        "accounts/home.html",
        {
            "form": form,
            "show_password": show_password
        }
    )


def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "ثبت‌نام و ورود موفقیت‌آمیز بود!")
        if user.role == "admin":
            return redirect("accounts:admin_panel")
        return redirect("accounts:customer_home")
    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "شما با موفقیت خارج شدید.")
    return redirect("home")


# Function-Based View برای داشبورد ادمین
@admin_required
def admin_panel(request):
    """
    صفحه اصلی پنل مدیریت
    فقط ادمین‌ها به این صفحه دسترسی دارند
    """
    context = {
        'admin_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'accounts/admin_panel.html', context)


# Class-Based View برای داشبورد ادمین (روش جایگزین)
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """
    صفحه اصلی پنل مدیریت - نسخه Class-Based
    """
    template_name = 'accounts/admin_panel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_name'] = self.request.user.get_full_name() or self.request.user.username
        return context
    
@login_required_custom
def wallet_view(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = WalletTopUpForm(request.POST)
        if form.is_valid():
            wallet.balance += form.cleaned_data["amount"]
            wallet.save(update_fields=["balance"])
            messages.success(request, "اعتبار کیف پول با موفقیت افزایش یافت.")
            return redirect("accounts:wallet")
    else:
        form = WalletTopUpForm()

    return render(
        request,
        "accounts/wallet.html",
        {
            "wallet": wallet,
            "form": form,
        },
    )

@login_required_custom    
def customer_home(request):
    """
    صفحه اصلی مشتری
    فقط مشتری‌ها به این صفحه دسترسی دارند
    """
    context = {
        'customer_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'accounts/customer_home.html', context)

#صفحه مربوط به نمایش لیست سینما برای مشتری
@login_required_custom
def customer_cinema_list(request):
    query = request.GET.get("q", "").strip()
    cinemas = Cinema.objects.all()
    if query:
        cinemas = cinemas.filter(name__icontains=query)

    context = {
        "cinemas": cinemas,
        "query": query,
    }
    return render(request, "accounts/customer_cinema_list.html", context)


#صفحه مربوط به نمایش لیست فیلم های هر سینما برای مشتری

@login_required_custom
def customer_movie_list(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    
    # دریافت پارامترهای جستجو و فیلتر
    search = request.GET.get("search", "")
    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")

    # فیلم‌های مرتبط با سینما از طریق Screening
    movies = Movie.objects.filter(screening__cinema=cinema).distinct()

    # فیلتر جستجو
    if search:
        movies = movies.filter(title__icontains=search)

    # فیلتر ژانر
    if genre:
        movies = movies.filter(genre__icontains=genre)

    # فیلتر سال
    if year:
        movies = movies.filter(year=year)

    # لیست ژانرها برای فیلتر
    genres = Movie.objects.values_list("genre", flat=True).distinct()

    # لیست سال‌ها برای فیلتر
    years = Movie.objects.exclude(year__isnull=True).values_list("year", flat=True).distinct()

    context = {
        "cinema": cinema,
        "movies": movies,
        "genres": genres,
        "years": years,
        "search": search,
        "genre_selected": genre,
        "year_selected": year,
    }

    return render(request, "accounts/customer_movie_list.html", context)


@login_required_custom
def customer_movie_detail(request, cinema_id, movie_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    movie = get_object_or_404(Movie, id=movie_id)

    screenings = (
        Screening.objects.select_related("showtime")
        .filter(cinema=cinema, movie=movie)
        .order_by("showtime__date", "showtime__start_time")
    )

    selected_screening_id = request.GET.get("screening")
    selected_screening = None
    if selected_screening_id:
        selected_screening = screenings.filter(id=selected_screening_id).first()

    context = {
        "cinema": cinema,
        "movie": movie,
        "screenings": screenings,
        "selected_screening": selected_screening,
    }
    return render(request, "accounts/customer_movie_detail.html", context)