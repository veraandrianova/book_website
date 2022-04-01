from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class Author(models.Model):
    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    firstname = models.CharField('имя', max_length=70)
    lastname = models.CharField('фамилия', max_length=70)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(default='', null=False, blank=True)
    name = models.CharField(max_length=70, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Author, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('author_details', args=[self.slug])

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class PubHouse(models.Model):
    class Meta:
        verbose_name = 'издание'
        verbose_name_plural = 'издания'

    name_house = models.CharField('название издательства', max_length=70)
    email = models.CharField('почта', max_length=70)
    slug = models.SlugField(default='', null=False, blank=True)
    address = models.CharField('адрес', max_length=200, default='', null=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name_house, 'ru', reversed=True))
        super(PubHouse, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('pub_house_details', args=[self.slug])

    def __str__(self):
        return f"{self.name_house}"


class BookPlace(models.Model):
    class Meta:
        verbose_name = 'место книги'
        verbose_name_plural = 'места книг'

    rack = models.IntegerField('стелаж', validators=[MinValueValidator(1),
                                                     MaxValueValidator(100)])
    number = models.IntegerField('порядковый норме', validators=[MinValueValidator(1),
                                                                 MaxValueValidator(100)])

    def __str__(self):
        return f"{self.rack}.{self.number}"


class Book(models.Model):
    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    COVER_CHOICES = [
        ('solid', 'Твердый переплет'),
        ('soft', 'Мягкий переплет'),
    ]

    title = models.CharField('название', max_length=70)
    description = models.TextField("Описание", blank=True)
    rating = models.IntegerField('Рейтинг', validators=[MinValueValidator(1),
                                                        MaxValueValidator(100)], blank=True)
    is_best_selling = models.BooleanField(null=True, blank=True)
    slug = models.SlugField(default='', null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    cover = models.CharField('переплет', max_length=10, choices=COVER_CHOICES, default='solid')
    pub_house = models.ManyToManyField(PubHouse)
    book_place = models.OneToOneField(BookPlace, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Book, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('book_details', args=[self.slug])

    def __str__(self):
        return f"{self.title} - {self.rating}"


class Customer(AbstractUser):
    SEX_CHOICES = [
            ('male', 'Мужской'),
            ('female', 'Женский'),
        ]

    phone = models.CharField('телефон', validators=[], max_length=13)
    age = models.IntegerField('возраст', validators=[MinValueValidator(1),
                                                     MaxValueValidator(100)], default=18)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male', verbose_name='пол')

    # class Users(models.Model):
    #     class Meta:
    #         verbose_name = 'пользователь'
    #         verbose_name_plural = 'пользователи'
    #
    #     SEX_CHOICES = [
    #         ('male', 'Мужской'),
    #         ('female', 'Женский'),
    #     ]
    #     firstname = models.CharField('имя', max_length=70)
    #     lastname = models.CharField('фамилия',max_length=70)
    #     email = models.EmailField('почта', max_length=254)
    #     phone = models.CharField('телефон', max_length=13)
    #     age = models.IntegerField('возраст', validators=[MinValueValidator(1),
    #                                              MaxValueValidator(100)], default=18)
    #     sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male', verbose_name='пол')
    #     books = models.ManyToManyField(Book)
    #

    # @property
    #  def age(self):
    #      return self._age
    # @age.setter
    #  def age(self, value):
    #      if not value.isdigit() or and value.isalpha():
    #         raise ValueError("Поле должно содержать цифры")
    #      self._age = value
    # @property
    #  def firstname(self):
    #      return self._firstname
    # @firstname.setter
    #  def firstname(self, value):
    #      if isinstance(value, str) and not value.isdigit() and value.isalpha():
    #          self._firstname = firstname
    #      raise ValueError("Поле должно содержать буквы")
    #
    # @property
    #  def lastname(self):
    #      return self._lastname
    # @lastname.setter
    #  def lastname(self, value):
    #      if isinstance(value, str) and not value.isdigit() and value.isalpha():
    #          self._lastname = lastname
    #      raise ValueError("Поле должно содержать буквы")
    #
    # @property
    #  def email(self):
    #      return self._email
    # @email.setter
    #  def email(self, value):
    #      if ('@' in value) and value.isalpha():
    #          self._email = email
    #      raise ValueError("Поле должно быть вида: csu23@mail.ru")
    #
    # @property
    #  def phone(self):
    #      return self._phone
    # @phone.setter
    #  def phone(self, value):
    #      if ('+' in value[0]) and value.isdigit() and not value.isalpha():
    #          self._phone = phone
    #      raise ValueError("Поле должно содержать цифры")
    #

    def get_absolute_url(self):
        return reverse('one_user', args=[str(self.id)])
