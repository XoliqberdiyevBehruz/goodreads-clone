from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTestCase(TestCase):
    def test_home_page(self):
        book = Book.objects.create(title='New Book', description='Nice book', isbn='54155523')
        user = CustomUser.objects.create(username='Behruz', first_name='Behruz', last_name='Xoliqberdiyev', email='xoliqberdiyevbehhruz@gmail.com')
        user.set_password('somepass')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Nice Book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='hmm')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=2, comment='Nice Book')

        response = self.client.get(reverse('home') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
