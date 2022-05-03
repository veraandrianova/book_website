from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from user.models import Customer




class Author(models.Model):
    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    firstname = models.CharField('имя', max_length=70)
    lastname = models.CharField('фамилия', max_length=70)
    image = models.ImageField("Постер", upload_to="movies/", blank=True)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(default='', null=False, blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f'{self.firstname} {self.lastname}', 'ru', reversed=True))
        super(Author, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('author_details', args=[self.slug])

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class PubHouse(models.Model):
    class Meta:
        verbose_name = 'издание'
        verbose_name_plural = 'издания'

    name_house = models.CharField('название издательства', max_length=70, unique=True)
    email = models.EmailField('почта', max_length=70)
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

    title = models.CharField('название', max_length=70, unique=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Постер", upload_to="photos/", blank=True)
    rating = models.IntegerField('Рейтинг', validators=[MinValueValidator(1),
                                                        MaxValueValidator(100)], blank=True, null=True)
    is_best_selling = models.BooleanField(null=True, blank=True)
    slug = models.SlugField(default='', null=False)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name='автор')
    cover = models.CharField('переплет', max_length=10, choices=COVER_CHOICES, default='solid')
    pub_house = models.ManyToManyField(PubHouse, verbose_name='издательство')
    book_place = models.OneToOneField(BookPlace, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey('user.Customer', on_delete=models.CASCADE, verbose_name='создатель')


    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_details', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} - {self.rating}"



class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comment_book')
    creator = models.ForeignKey('user.Customer', on_delete=models.CASCADE, default=1, verbose_name='автор комментария')
    body = models.TextField('текст')
    created = models.DateTimeField('создано',auto_now_add=True)
    updated = models.DateTimeField('измененно', auto_now=True)
    active = models.BooleanField('активность', default=True)

    class Meta:
        verbose_name = 'комментрарий'
        verbose_name_plural = 'комментарии'
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.creator, self.book)

