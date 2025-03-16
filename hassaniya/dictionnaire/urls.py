from django.urls import path
from .views import register, user_login, user_logout, profile, users_list, update_user, delete_user, contributions_list, validate_contribution, add_comment, suggest_word, search_word, list_words, add_word, update_word, delete_word, user_contributions, view_comments, reply_to_comment

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('users/', users_list, name='users_list'),
    path('users/update/<int:id>/', update_user, name='update_user'),
    path('users/delete/<int:id>/', delete_user, name='delete_user'),
    path('contributions/', contributions_list, name='contributions_list'),
    path('contributions/validate/<int:id>/', validate_contribution, name='validate_contribution'),
    path('contributions/comment/<int:id>/', add_comment, name='add_comment'),
    path('contributions/suggest/', suggest_word, name='suggest_word'),
    path('search/', search_word, name='search_word'),
    path('dictionnaire', list_words, name='list_words'),
    path('word/add/', add_word, name='add_word'),
    path('word/update/<int:id>/', update_word, name='update_word'),
    path('word/delete/<int:id>/', delete_word, name='delete_word'),
    path('my-contributions/', user_contributions, name='user_contributions'),
    path('view-comments/<int:contribution_id>/<int:commenter_id>/', view_comments, name='view_comments'),
    path('reply-to-comment/<int:contribution_id>/<int:commenter_id>/', reply_to_comment, name='reply_to_comment'),
]