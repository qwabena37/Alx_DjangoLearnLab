from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),

    # REQUIRED MANUAL LIKE/UNLIKE PATHS
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'})),      # <-- REQUIRED STRING
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'})),  # <-- REQUIRED STRING
]
