from django.urls import path

from book import views

urlpatterns = [
    path('', views.all_books, name='books'),
    path('accaunts', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('add_book/', views.AddBook.as_view(), name="add_book"),
    # path('users/', views.CreateUser.as_view(), name='new_user'),
    # path('users/', views.users_create, name='new_users'),
    # path('users/<int:id>/', views.one_create, name='one_user'),
    path('users/<int:pk>/update', views.ProfileEditView.as_view(), name='update_user'),
    path('book/<slug:slug_book>/', views.one_books, name='book_details'),
    path('author/', views.all_authors),
    path('author/<slug:slug_author>/', views.one_author, name='author_details'),
    path('pub_house/', views.all_pub_houses),
    path('pub_house/<slug:slug_pub_house>/', views.one_pub_house, name='pub_house_details'),
]
