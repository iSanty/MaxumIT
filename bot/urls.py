from django.urls import path
from .views import bot, bot_saladillo




urlpatterns = [
    path('', bot_saladillo),
]

