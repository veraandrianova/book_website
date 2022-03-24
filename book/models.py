from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    firstname = models.CharField(max_length=70)
    lastname = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
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
    name_house = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    slug = models.SlugField(default='', null=False, blank=True)
    address  = models.CharField(max_length=200, default='', null=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name_house, 'ru', reversed=True))
        super(PubHouse, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('pub_house_details', args=[self.slug])

    def __str__(self):
        return f"{self.name_house}"


class Book_Place(models.Model):
    rack = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    number  = models.IntegerField(validators=[MinValueValidator(1),
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

    title = models.CharField(max_length=70, verbose_name='название')
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    is_best_selling = models.BooleanField(null=True, blank=True)
    slug = models.SlugField(default='', null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    cover = models.CharField(max_length=10, choices=COVER_CHOICES, default='solid', verbose_name='переплет')
    pub_house = models.ManyToManyField(PubHouse)
    book_place = models.OneToOneField(Book_Place, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Book, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('book_details', args=[self.slug])

    def __str__(self):
        return f"{self.title} - {self.rating}"


