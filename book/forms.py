from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import Customer, Book
from django.core.exceptions import ValidationError
from django import forms
from django.core.exceptions import ValidationError

# class CustomForm(forms.Form):
#     test_field = forms.CharField(max_length=10, label='test')
#     num_field = forms.IntegerField(max_value=20, label='num')

class CustomerForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    firstname = forms.CharField(label='Имя')
    lastname = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Электронная почта')
    phone = forms.CharField(label='Телефон')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')



    class Meta:
        model = Customer
        fields = ("username", 'firstname', 'lastname', 'email', 'phone',  'sex', 'age')
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


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'rating', 'description', 'author']

