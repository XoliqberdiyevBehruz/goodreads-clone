from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview

def landing_page(request):
    return render(request, 'landing_page.html')

def home_page(request):
    reviews = BookReview.objects.all().order_by('-created_at')

    page_size = request.GET.get('page_size', 10)
    pagination = Paginator(reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_obj = pagination.get_page(page_num)

    return render(request, 'home.html', {"page_obj":page_obj})