from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from .validators import phone_validator
# Create your models here.


class Customer(AbstractUser):

    class Meta:
        app_label = 'user'
    SEX_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    phone = models.CharField('телефон', validators=[phone_validator], max_length=13)
    age = models.IntegerField('возраст', validators=[MinValueValidator(1),
                                                     MaxValueValidator(100)], default=18)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male', verbose_name='пол')
    #
    # def get_absolute_url(self):
    #     return reverse('user_detail', args=[str(self.id)])
