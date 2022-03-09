from book import views
from django.urls import path


urlpatterns = [
    path('', views.all_books),
    path('book/<slug:slug_book>', views.one_books, name = 'book_details'),
]
