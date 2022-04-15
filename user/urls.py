from django.urls import path

from user import views
from user.views import LoginUser, logout_user

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='delete_user'),
    path('users/<int:pk>/update/', views.ProfileEditView.as_view(), name='update_user'),
]
