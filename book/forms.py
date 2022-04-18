from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import Textarea
from .models import Book, Comment



class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'rating', 'description', 'author', 'pub_house']

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'description',
            'image',
            'rating',
            'author',
            'pub_house'
        ]


class RewiewForm(forms.ModelForm):
    body = forms.CharField(label='', widget=Textarea(attrs={'rows': 5}))


    class Meta:
        model = Comment
        fields = ["body"]
