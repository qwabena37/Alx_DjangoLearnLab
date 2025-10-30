
✅ **Explanation:**
- `.get()` fetches the book you previously created.  
- You change the `title` attribute.  
- `.save()` writes the updated value to the database.  
- Finally, you check that the update worked by printing `book.title`.

---

## 🟥 **delete.md**

**Goal:** Delete the updated book (“Nineteen Eighty-Four”) and confirm that it no longer exists in the database.

```markdown
# Delete Operation

```python
from bookshelf.models import Book

# Retrieve the Book instance by title
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the Book instance from the database
book.delete()

# Confirm deletion by checking all Book records
Book.objects.all()
# Expected Output: <QuerySet []>
