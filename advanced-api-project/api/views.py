from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['publication_year', 'title']
    permission_classes = [AllowAny]
def get_queryset(self):
    # Optional custom filtering
    return Book.objects.filter(publication_year__lte=2025)



class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single Book instance by its primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        """
        Custom logic when a book is created.
        Could log events, enforce constraints, etc.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
