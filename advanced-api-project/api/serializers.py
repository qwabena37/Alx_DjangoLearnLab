from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book objects.
    Includes custom validation to ensure publication_year
    cannot be set in the future.
    """

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author objects.
    Includes nested BookSerializer to show all books written by the author.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
