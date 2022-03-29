from book import views
from django.urls import path


urlpatterns = [
    path('', views.all_books, name='book'),
    path('users/', views.users_create, name='new_users'),
    path('users/<int:id>/', views.one_create, name='one_user'),
    path('users/<int:id>/update', views.NewsUpdateNew.as_view(), name='create_update'),
    path('book/<slug:slug_book>/', views.one_books, name='book_details'),
    path('author/', views.all_authors),
    path('author/<slug:slug_author>/', views.one_author, name='author_details'),
    path('pub_house/', views.all_pub_houses),
    path('pub_house/<slug:slug_pub_house>/', views.one_pub_house, name='pub_house_details'),
]
