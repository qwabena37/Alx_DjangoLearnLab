# 📘 **Advanced API Project — Django REST Framework**

A fully implemented Django REST Framework project designed to teach and demonstrate:

* Custom serializers
* Nested model relationships
* Generic views & mixins
* Custom view behavior
* Permission handling
* Organized URL routing
* API documentation & testing

This project manages **Authors** and their **Books**, providing a complete CRUD API while keeping the structure easy to understand and extend.


# 🚀 **Project Features**

### ✔️ Django REST Framework setup

### ✔️ Models for `Author` and `Book`

### ✔️ Nested serialization (Author → Books)

### ✔️ Custom validation in serializers

### ✔️ Generic class-based views

### ✔️ CRUD operations for Books

### ✔️ Permissions (authenticated vs. read-only access)

### ✔️ Clean URL routing

### ✔️ Ready for testing via Postman, curl, or DRF’s browsable API

---

# 📦 **1. Project Setup**

### Create Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

### Install Dependencies

```bash
pip install django djangorestframework
```

### Create Django Project

```bash
django-admin startproject advanced_api_project .
```

### Create API App

```bash
python manage.py startapp api
```

---

# 🏗️ **2. Application Structure**

```
advanced-api-project/
│
├── advanced_api_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
└── README.md
```

---

# 🧩 **3. Models**

Defined in `api/models.py`.

### **Author**

* `name` — CharField

### **Book**

* `title` — CharField
* `publication_year` — IntegerField
* `author` — ForeignKey → Author (one-to-many)

### Relationship

One Author can have **many** Books.
This is exposed through `related_name="books"`.

---

# 🔧 **4. Serializers**

Defined in `api/serializers.py`.

### **BookSerializer**

* Serializes all fields of `Book`.
* Includes **custom validation** preventing future publication years.

### **AuthorSerializer**

* Serializes `name`
* Includes **nested BookSerializer** to automatically list all books belonging to the Author.

---

# 🌐 **5. Views (Generic Class-Based Views)**

Defined in `api/views.py`.

### **BookListView**

* Type: `ListAPIView`
* Purpose: View all books
* URL: `/api/books/`

### **BookDetailView**

* Type: `RetrieveAPIView`
* Purpose: View details of one book
* URL: `/api/books/<pk>/`

### **BookCreateView**

* Type: `CreateAPIView`
* Purpose: Add a new book
* URL: `/api/books/create/`
* Permissions: Authenticated users only
* Custom behavior: validation & optional custom `perform_create`

### **BookUpdateView**

* Type: `UpdateAPIView`
* Purpose: Edit an existing book
* URL: `/api/books/<pk>/update/`
* Permissions: Authenticated users only

### **BookDeleteView**

* Type: `DestroyAPIView`
* Purpose: Remove a book
* URL: `/api/books/<pk>/delete/`
* Permissions: Authenticated users only

### Customizations

* Permissions added directly on views
* Optional hooks:

  * `perform_create()`
  * `perform_update()`
  * `get_queryset()` for filtering
  * DRF filters (ordering, searching)

---

# 🛡️ **6. Permissions**

Using DRF permission classes:

### Public (no authentication required)

* **ListView**
* **DetailView**

### Authenticated Users Only

* **CreateView**
* **UpdateView**
* **DeleteView**

Set via:

```python
permission_classes = [IsAuthenticated]
```

or

```python
permission_classes = [AllowAny]
```

---

# 🔗 **7. URL Routing**

Project-level (`advanced_api_project/urls.py`):

```python
urlpatterns = [
    path('api/', include('api.urls')),
]
```

API-level (`api/urls.py`):

```
/api/books/                    → List all books  
/api/books/<id>/               → Retrieve one book  
/api/books/create/             → Create a book  
/api/books/<id>/update/        → Update a book  
/api/books/<id>/delete/        → Delete a book  
```

---

# 🧪 **8. Testing the API**

You can test via:

* ✔️ Postman
* ✔️ curl
* ✔️ DRF Browsable API at:
  `http://127.0.0.1:8000/api/books/`

### Example Test Requests

#### Create a Book (POST)

```json
{
  "title": "Example Book",
  "publication_year": 2022,
  "author": 1
}
```

#### Update a Book (PUT/PATCH)

```json
{
  "title": "Updated Title"
}
```

#### Delete a Book

Send a DELETE request to:

```
/api/books/<id>/delete/
```

### Filtering
Use query parameters like:
  /api/books/?title=Example

### Searching
Use:
  /api/books/?search=keyword

### Ordering
Use:
  /api/books/?ordering=title
  /api/books/?ordering=-publication_year


### Permission Testing

Try requests:

* 🔓 **Logged out** → Only GET should work
* 🔐 **Logged in** → Can POST, PUT, DELETE

---

# 📄 **9. Documentation & Comments**

All views, serializers, and models contain comments explaining:

* Purpose of each class
* Relationships between models
* How nested serialization works
* Why specific permissions were chosen
* Custom behavior (filters, hooks, validation)

---

# 🧱 **10. Future Extensions (Optional Ideas)**

You can expand the project with:

* Pagination
* Searching/Filtering
* Token or JWT authentication
* Custom permissions
* ViewSets + Routers
* Swagger/OpenAPI docs
