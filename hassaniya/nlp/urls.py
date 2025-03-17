from django.urls import path
from .views import transform_word

urlpatterns = [
    path('traduction/', transform_word, name='traduction'),
]
