# Update Operation

```python
from bookshelf.models import Book

# Retrieve the Book instance by title
book = Book.objects.get(title="1984")

# Update the title field
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Confirm that the update was successful
book.title
# Expected Output: 'Nineteen Eighty-Four'
