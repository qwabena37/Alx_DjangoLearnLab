from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return author.books.all()

# Query 2: All books in a specific library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Query 3: Retrieve the librarian for a specific library
def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian


if __name__ == "__main__":
    # Example usage (adjust names as needed)
    print("Books by J.K. Rowling:")
    print(books_by_author("J.K. Rowling"))

    print("\nBooks in Central Library:")
    print(books_in_library("Central Library"))

    print("\nLibrarian of Central Library:")
    print(librarian_of_library("Central Library"))
