from django.urls import path
from .views import chat_text, chat_image, home

urlpatterns = [
    path('', home, name='home'),
    path('chat_text/', chat_text, name='chat_text'),
    path('chat_image/', chat_image, name='chat_image'),
]
