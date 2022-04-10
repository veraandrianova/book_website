from django.urls import path

from book import views
from book.views import LoginUser, logout_user

urlpatterns = [
    path('', views.BookAll.as_view(), name='books'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('add_book/', views.AddBook.as_view(), name="add_book"),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/<int:pk>/delete', views.ProfileDeleteView.as_view(), name='delete_user'),
    path('users/<int:pk>/update', views.ProfileEditView.as_view(), name='update_user'),
    path('book/<slug:slug_book>/', views.ShowBook.as_view(), name='book_details'),
    path('book/<slug:slug_book>/update', views.BookEditView.as_view(), name='book_edit'),
    path('book/<slug:slug_book>/delete', views.BookDeleteView.as_view(), name='book_delete'),
    path('author/', views.AuthorAll.as_view(), name='author'),
    path('author/<slug:slug_author>/', views.ShowAuthor.as_view(), name='author_details'),
    path('pub_house/', views.PubHouseAll.as_view(), name='pub_house'),
    path('pub_house/<slug:slug_pub_house>/', views.ShowPubHouse.as_view(), name='pub_house_details'),
]
