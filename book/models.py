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
    image = models.ImageField("Постер", upload_to="movies/", blank=True)
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
    image = models.ImageField("Постер", upload_to="photos/", blank=True)
    rating = models.IntegerField('Рейтинг', validators=[MinValueValidator(1),
                                                        MaxValueValidator(100)], blank=True)
    is_best_selling = models.BooleanField(null=True, blank=True)
    slug = models.SlugField(default='', null=False)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    cover = models.CharField('переплет', max_length=10, choices=COVER_CHOICES, default='solid')
    pub_house = models.ManyToManyField(PubHouse)
    book_place = models.OneToOneField(BookPlace, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_details', kwargs={'slug_book': self.slug})

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



    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])
