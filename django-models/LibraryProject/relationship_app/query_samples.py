from relationship_app.models import Author, Book, Library, Librarian


# Query 1: All books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    # Using the related_name approach:
    books_via_related = author.books.all()
    # Using the objects.filter() method explicitly:
    books_via_filter = Book.objects.filter(author=author)

    print(f"\nBooks by {author_name} (via related_name):")
    for book in books_via_related:
        print(f" - {book.title}")

    print(f"\nBooks by {author_name} (via objects.filter):")
    for book in books_via_filter:
        print(f" - {book.title}")

    return books_via_filter


# Query 2: All books in a specific library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()

    print(f"\nBooks in {library_name}:")
    for book in books:
        print(f" - {book.title}")

    return books


# Query 3: Retrieve the librarian for a specific library
def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian

    print(f"\nLibrarian of {library_name}: {librarian.name}")
    return librarian


if __name__ == "__main__":
    # Example usage (adjust names as needed)
    books_by_author("J.K. Rowling")
    books_in_library("Central Library")
    librarian_of_library("Central Library")
