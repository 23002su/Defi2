from django.urls import path
from .views import register, user_login, user_logout, profile, users_list, update_user, delete_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('users/', users_list, name='users_list'),
    path('users/update/<int:id>/', update_user, name='update_user'),
    path('users/delete/<int:id>/', delete_user, name='delete_user'),
]