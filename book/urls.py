from django.urls import path
from .views import BookAPIView, ResidentAPIView, AvailabilityAPIView

app_name = 'book'

urlpatterns = [
    path('rooms/<int:pk>/book/', BookAPIView.as_view(), name='book'),

    path('resident/', ResidentAPIView.as_view(), name='resident'),
    path('rooms/<int:pk>/availability/', AvailabilityAPIView.as_view(), name='room-availability'),
]    

