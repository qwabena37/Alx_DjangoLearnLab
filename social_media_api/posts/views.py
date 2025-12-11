from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        """
        POST /api/posts/{pk}/like/
        Creates a Like if not exists and creates a Notification.
        """
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        # prevent anonymous
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        # prevent liking own post? optional - allow or disallow:
        # if post.author == user: return Response(...)

        like, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # create notification -- import lazily to avoid circular imports
        from notifications.utils import create_notification
        create_notification(recipient=post.author, actor=user, verb='liked', target=post)

        serializer = LikeSerializer(like, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def unlike(self, request, pk=None):
        """
        POST /api/posts/{pk}/unlike/
        Removes a Like if exists.
        """
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            like = Like.objects.get(post=post, user=user)
        except Like.DoesNotExist:
            return Response({'detail': 'Like does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        # Optionally create an "unliked" notification or remove previous like-notification.
        return Response({'detail': 'Unliked.'}, status=status.HTTP_204_NO_CONTENT)
