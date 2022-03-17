from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from django.core.validators import MinValueValidator, MaxValueValidator

class Autor(models.Model):
    firstname = models.CharField(max_length=70)
    lastname = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Year(models.Model):
    name = models.CharField(max_length=70)
    year = models.IntegerField(validators=[MinValueValidator(1000),
                                             MaxValueValidator(2030)])
    def __str__(self):
        return f"{self.year}"


class Book(models.Model):
    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'


    title = models.CharField(max_length=70, verbose_name='название')
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    is_best_selling = models.BooleanField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', null=False)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    year = models.ManyToManyField(Year)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Book, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('book_details', args=[self.slug])

    def __str__(self):
        return f"{self.title} - {self.rating}"
