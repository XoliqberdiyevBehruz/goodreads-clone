from rest_framework.views import APIView
from rest_framework.response import Response
from books.models import BookReview
from .serializers import BookReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets




class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')
    lookup_field = 'id'

    # def get(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(book_review)

    #     return Response(data=serializer.data)

    # def delete(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     book_review.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def put(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(instance=book_review, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()

    #         return Response(serializer.data, status=status.HTTP_200_OK)
        
    #     return Response(
    #         {
    #             'success':False,
    #             'message':'Updated unsuccessfully'
    #         }
    #     )



class BookListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')


    # def get(self, request):
    #     book_review = BookReview.objects.all().order_by('-created_at')

    #     paginator = PageNumberPagination()
    #     page_obj = paginator.paginate_queryset(book_review, request )
    #     serializer = BookReviewSerializer(page_obj, many=True)
        
    #     return paginator.get_paginated_response(serializer.data)

    # def post(self, request):
    #     serializer = BookReviewSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    