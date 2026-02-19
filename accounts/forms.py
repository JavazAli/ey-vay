from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="شماره تلفن",
        widget=forms.TextInput(attrs={
            "placeholder": "شماره تلفن خود را وارد کنید",
            "class": "form-control"
        })
    )
    password = forms.CharField(
        label="رمز عبور",
        required=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "رمز عبور خود را وارد کنید",
            "class": "form-control"
        })
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and not phone.isdigit():
            raise forms.ValidationError("شماره تلفن فقط می‌تواند شامل اعداد باشد.")
        return phone


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="نام", max_length=30)
    last_name = forms.CharField(label="نام خانوادگی", max_length=30)
    phone_number = forms.CharField(label="شماره تلفن", max_length=15)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "phone_number", "password1", "password2")

    # اضافه کردن ولیدیشن برای شماره تلفن
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.isdigit():
            raise forms.ValidationError("شماره تلفن فقط می‌تواند شامل اعداد باشد.")
        return phone
