📘 Social Media API — README

A Django-based REST API for a simple social media platform.
This initial version includes project setup, custom user model, and token-based authentication (register, login, and profile endpoints).

🚀 Features

Custom User Model with:

bio

profile_picture

followers (Many-to-Many)

User Registration

User Login

Token Authentication

User Profile Endpoint

Django REST Framework Integration

Clean project structure for future expansion (posts, comments, likes, etc.)

🛠 Tech Stack
Tool	Purpose
Django	Backend Framework
Django REST Framework (DRF)	API development
DRF Token Authentication	User authentication
SQLite (default)	Database
📂 Project Structure
social_media_api/
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── apps.py
│
├── manage.py
└── README.md

⚙️ Installation & Setup
1. Clone the Project
git clone <repo-url>
cd social_media_api

2. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate   # macOS/Linux

3. Install Dependencies
pip install django djangorestframework
pip install djangorestframework-simplejwt


(If you already installed them, skip this.)

🧩 Project Initialization
Run Migrations
python manage.py makemigrations
python manage.py migrate

Start the Development Server
python manage.py runserver


Server runs at:
👉 http://127.0.0.1:8000/

🔐 Authentication Endpoints

All authentication routes are located under:

/auth/

1. Register User
POST /auth/register/
Example Body:
{
  "username": "james",
  "email": "james@example.com",
  "password": "mypassword123"
}

Response:

A success message

Authentication token

2. Login User
POST /auth/login/
Body:
{
  "username": "james",
  "password": "mypassword123"
}

Response:

Token for authenticated operations

3. Get User Profile
GET /auth/profile/
Required Header:
Authorization: Token <your_token_here>

Response:

User info including followers count and bio.

🧪 Testing With Postman

You can test each route by:

Sending JSON body requests to /auth/register/ and /auth/login/

Copying the returned token

Adding it to headers:

Authorization: Token YOUR_TOKEN


Calling /auth/profile/

📄 Custom User Model

The project uses a custom user model (accounts.User) that extends Django’s AbstractUser.

Extra fields:

bio

profile_picture

followers

This allows easier expansion later (posts, likes, comments, messaging, etc.)

🚧 Future Enhancements

Planned features include:

Post creation & feeds

Comments

Likes

Follow system endpoints

Notifications

User search

Profile update endpoint

JWT authentication option

🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to modify.
