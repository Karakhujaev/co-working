from django.urls import path
from .views import RoomCreateAPIView, RoomDetailAPIView, RoomAPIView

app_name = 'room'

urlpatterns = [
    path('rooms/', RoomAPIView.as_view(), name='room-list'),
    path('room/create/', RoomCreateAPIView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
]

