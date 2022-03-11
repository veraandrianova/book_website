from django.contrib import admin
from .models import Book
# Register your models here.
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
    list_display = ['title', 'rating', 'is_best_selling', 'author', 'rating_status']
    list_editable = ['rating', 'is_best_selling', 'author']
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
admin.site.register(Book, BookAdmin)

