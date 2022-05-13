from django.urls import path

from book import views


urlpatterns = [
    path('', views.BookAll.as_view(), name='books'),
    path('add_book/', views.AddBook.as_view(), name="add_book"),
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<slug:slug>/', views.ShowBook.as_view(), name='book_details'),
    path('book/<slug:slug>/update/', views.BookEditView.as_view(), name='book_edit'),
    path('book/<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('author/', views.AuthorAll.as_view(), name='author'),
    path('author/<slug:slug>/', views.ShowAuthor.as_view(), name='author_details'),
    path('pub_house/', views.PubHouseAll.as_view(), name='pub_house'),
    path('pub_house/<slug:slug>/', views.ShowPubHouse.as_view(), name='pub_house_details'),
]
