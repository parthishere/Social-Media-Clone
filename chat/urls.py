from django.urls import path

from .views import index, room

app_name = 'chat'

urlpatterns = [
    path('', index, name='home'),
    path('<str:room_id>', room, name='room'),
]