from django.urls import path
from .views import BookAPIView

app_name = 'book'

urlpatterns = [
    path('book/', BookAPIView.as_view(), name='book'),
]
