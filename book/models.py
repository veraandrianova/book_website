from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=70)
    rating = models.IntegerField()
    is_best_selling = models.BooleanField(null = True)
    author = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', null=False)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


    def get_url(self):
        return reverse('book_details', args=[self.slug])


    def __str__(self):
        return f"{self.title} - {self.rating}"
