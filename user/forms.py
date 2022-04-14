from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import Textarea
from .models import Customer


class CustomerForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Электронная почта')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')
    captcha = CaptchaField(label='Введите код с картинки')

    class Meta:
        model = Customer
        fields = ("username", 'email')
        field_classes = {"username": UsernameField}

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone[1:].isdigit():
            raise ValidationError('Поле должно быть формата +79876543211')
        if phone[0] != '+':
            raise ValidationError('Поле должно быть формата +79876543211')
        if len(phone) != 12:
            raise ValidationError('Поле должно быть формата +79876543211')
        return phone


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'age',
            'sex'
        ]





class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


