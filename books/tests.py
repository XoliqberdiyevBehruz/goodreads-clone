from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No found book')

    def test_books_list(self):
        Book.objects.create(title='book1', description='book1', isbn='123456789')
        Book.objects.create(title='book2', description='book2', isbn='1234567')
        Book.objects.create(title='book3', description='book3', isbn='12345678')

        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)

    def test_search_books(self):
        book1 = Book.objects.create(title='Steve', description='book1', isbn='123456789')
        book2 = Book.objects.create(title='Doe Shu', description='book2', isbn='1234567')
        book3 = Book.objects.create(title='Ilon Mask', description='book3', isbn='12345678')

        response = self.client.get(reverse('books:list') + '?q=Steve')

        self.assertContains(response, book1)
        self.assertNotContains(response, book2)
        self.assertNotContains(response, book3)

    def test_book_detail(self):
        book = Book.objects.create(title='book1', description='book1', isbn='123456789')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
