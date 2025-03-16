from django.urls import path
from .views import register, user_login, user_logout, profile, users_list, update_user, delete_user, contributions_list, validate_contribution, add_comment, suggest_word

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('users/', users_list, name='users_list'),
    path('users/update/<int:id>/', update_user, name='update_user'),
    path('users/delete/<int:id>/', delete_user, name='delete_user'),
    path('contributions/', contributions_list, name='contributions_list'),
    path('contributions/validate/<int:id>/', validate_contribution, name='validate_contribution'),
    path('contributions/comment/<int:id>/', add_comment, name='add_comment'),
    path('contributions/suggest/', suggest_word, name='suggest_word'),
]