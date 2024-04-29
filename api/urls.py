from django.urls import path
from .views import BookDetailAPIView, BookListAPIView


app_name = 'api'


urlpatterns  = [
    path('reviews/<int:id>/', BookDetailAPIView.as_view(), name='detail'),
    path('reviews/', BookListAPIView.as_view(), name='list'),

]