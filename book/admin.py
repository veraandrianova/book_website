from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, Author, PubHouse, BookPlace, Comment
from django.utils.translation import gettext_lazy as _


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('>=40 and <75', 'Средний'),
            ('>=75', 'Высокий')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == '>=40 and <75':
            return queryset.filter(rating__gte=40).filter(rating__lt=75)
        if self.value() == '>=75':
            return queryset.filter(rating__gte=75)


class BookAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['title', 'rating', 'is_best_selling', 'rating_status']
    list_editable = ['rating', 'is_best_selling']
    filter_horizontal = ['pub_house']
    ordering = ["title"]
    list_per_page = 10
    search_fields = ['title']
    list_filter = [RatingFilter]

    @admin.display(ordering='rating')
    def rating_status(self, book: Book):
        if book.rating < 50:
            return 'Зачем это читать?'
        if book.rating < 70:
            return 'На один раз'
        if book.rating <= 85:
            return 'Хорошая книга'
        return 'Отличный выбор'


class BookPlaceAdmin(admin.ModelAdmin):
    ordering = ["rack", "number"]


class AutorAdmin(admin.ModelAdmin):
    ordering = ["lastname"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'book', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('creator', 'body')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AutorAdmin)
admin.site.register(PubHouse)
admin.site.register(BookPlace, BookPlaceAdmin)
