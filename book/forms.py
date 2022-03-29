from django import forms
from .models import Users
from django.forms import ModelForm, TextInput

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        # fields = ['title', 'rating']
        fields = '__all__'
        # exclude = ['slug']
        widgets = {
            "firstname": TextInput(attrs={
                'placeholder': 'Имя'
            }),
            "lastname": TextInput(attrs={
                'placeholder': 'Фамилия'
            }),
            "email": TextInput(attrs={
                'placeholder': 'Электронная почта'
            }),
            "phone": TextInput(attrs={
                'placeholder': 'Телефон'
            })
        }


# class CustomForm(forms.Form):
#     test_field = forms.CharField(max_length=10, label='test')
#     num_field = forms.IntegerField(max_value=20, label='num')
