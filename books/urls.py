from django.urls import path

from .views import BookListView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteView, DeleteReviewView

app_name = 'books'
urlpatterns = [
    path("", BookListView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/reviews/', AddReviewView.as_view(), name='reviews'),
    path('<int:book_id>/review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit_review_view'),
    path('<int:book_id>/review/<int:review_id>/delete/confirm/', ConfirmDeleteView.as_view(), name='delete_confirm_review_view'),
    path('<int:book_id>/review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review_view'),


    
]