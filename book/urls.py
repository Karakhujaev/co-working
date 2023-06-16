from django.urls import path
from .views import BookAPIView, ResidentAPIView

app_name = 'book'

urlpatterns = [
    path('rooms/<int:pk>/book/', BookAPIView.as_view(), name='book'),

    path('resident/', ResidentAPIView.as_view(), name='resident'),
]
