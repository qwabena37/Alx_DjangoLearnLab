# Create Operation

```python
from bookshelf.models import Book

# Create and save a new Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
book
# Expected Output: <Book: 1984 by George Orwell>

# Exit the Django shell
exit()
