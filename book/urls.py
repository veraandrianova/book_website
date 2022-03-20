from book import views
from django.urls import path


urlpatterns = [
    path('', views.all_books),
    path('book/<slug:slug_book>/', views.one_books, name = 'book_details'),
    path('author/', views.all_authors),
    path('author/<slug:slug_author>/', views.one_author, name = 'author_details'),
    path('pub_house/', views.all_pub_houses),
    path('pub_house/<slug:slug_pub_house>/', views.one_pub_house, name = 'pub_house_details'),
]
