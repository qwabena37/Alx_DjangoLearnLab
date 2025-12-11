from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Post model.
    """
    # Explicit requirement for your system:
    queryset = Post.objects.all()  # <-- REQUIRED LINE

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Comment model.
    """
    # Explicit requirement for your system:
    queryset = Comment.objects.all()  # <-- REQUIRED LINE

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Optionally filter by post using query param
        queryset = Comment.objects.all()  # Keep this explicit for your system
        post_id = self.request.query_params.get('post')

        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset
