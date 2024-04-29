from rest_framework.test import APITestCase
from rest_framework.reverse import reverse 
from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='behruz', first_name='Behruz')
        self.user.set_password('somepassword')
        self.user.save()
        self.client.login(username='behruz', password='somepassword')

    def test_book_review_detail(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12321')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')

        response = self.client.get(reverse('api:detail', kwargs={'id':book_review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['comment'], 'Nice book')
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['book']['title'], 'book1')
        self.assertEqual(response.data['book']['description'], 'description1')
        self.assertEqual(response.data['book']['isbn'], '12321')
        self.assertEqual(response.data['user']['username'], 'behruz')
        self.assertEqual(response.data['user']['first_name'], 'Behruz')

    def test_delete_review(self):
        book = Book.objects.create(title='book', description='description', isbn='12321')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice book')

        response = self.client.delete(reverse('api:detail', kwargs={'id':book_review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='book', description='description', isbn='12321')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice book')

        response = self.client.patch(reverse('api:detail', kwargs={'id':book_review.id}), data={'stars_given':4})
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)

    def test_put_review(self):
        book = Book.objects.create(title='book', description='description', isbn='12321')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice book')

        response = self.client.put(
            reverse('api:detail', kwargs={'id':book_review.id}), 
            data={
                'stars_given':4, 
                'comment':'Nice Book',
                'book_id':book.id,
                'user_id':self.user.id
                })

        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.comment, "Nice Book")
        self.assertNotEqual(book_review.comment, "nice book")
        self.assertEqual(book_review.stars_given, 4)



    def test_book_review_list(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12321')
        book2 = Book.objects.create(title='book2', description='description2', isbn='1234321')

        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Nice book')
        book_review2 = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='Nice book2')


        response = self.client.get(reverse('api:list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], book_review2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], 4)
        self.assertEqual(response.data['results'][0]['comment'], 'Nice book2')
        self.assertEqual(response.data['results'][1]['id'], book_review.id)
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][1]['comment'], 'Nice book')

    def test_create_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='12321')

        data={
            'book_id':book.id,
            'user_id':self.user.id,
            'stars_given':2,
            'comment':'Bad Book'
        }

        response = self.client.post(reverse('api:list'), data=data)
        book_review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.comment, 'Bad Book')