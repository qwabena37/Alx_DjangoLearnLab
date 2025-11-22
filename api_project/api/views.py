from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework import viewsets, permissions



class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

