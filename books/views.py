from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from books.forms import BookReviewForm
from books.models import Book, BookReview
from django.contrib.auth.mixins import LoginRequiredMixin   
from django.contrib import messages

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')

        search_query = request.GET.get("q", '')

        
        if search_query:
            books = books.filter(title__icontains=search_query)
            

        page_size = request.GET.get('page_size', 4)
        paginator = Paginator(books, page_size)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)


        return render(request, 'books/book_list.html',
                    {'page_obj':page_obj,'search_query':search_query,})
    
class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        context = {
            'book':book,
            'review_form':review_form
        }
        return render(request, 'books/book_detail.html', context)
    

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment'],
            )
            return redirect(reverse('books:detail', kwargs={'id':book.id}))
        
        context = {
            'book':book,
            'review_form':review_form
        }
        return render(request, 'books/book_detail.html', context)


class EditReviewView(View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {
            'book':book,
            'review':review,
            'review_form':review_form
        }
        return render(request, 'books/edit-review.html', context)
    
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid:
            review_form.save()
            
            return redirect(reverse('books:detail', kwargs={'id': book.id}))
        context = {
            'book':book,
            'review':review,
            'review_form':review_form
        }
        return render(request, 'books/edit-review.html', context)
        

class ConfirmDeleteView(View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        context = {
            'book': book,
            'review': review
        }
        return render(request, 'books/confirm-delete.html', context)

class DeleteReviewView(View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)

        review.delete()
        messages.success(request, 'Review successfully deleted')

        return redirect(reverse('books:detail', kwargs={'id':book.id}))