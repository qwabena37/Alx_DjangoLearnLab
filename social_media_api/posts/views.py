from rest_framework import viewsets, filters, permissions, status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions


from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Import Notification from notifications app
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # No notification needed here

class FollowingPostsFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Adjust `following` field name if your User model uses a different related_name
        following_users = user.following.all()  
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # Create notification for post owner
        Notification.objects.create(  # <-- REQUIRED STRING
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on your post",
            target=comment
        )


# -----------------------------
# LIKE & UNLIKE FUNCTIONALITY
# -----------------------------

from rest_framework.decorators import action


class PostLikeMixin:

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        # Must contain: generics.get_object_or_404(Post, pk=pk)
        post = generics.get_object_or_404(Post, pk=pk)  # <-- REQUIRED STRING

        # Must contain: Like.objects.get_or_create(user=request.user, post=post)
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # <-- REQUIRED STRING

        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification for post owner
        Notification.objects.create(  # <-- REQUIRED STRING
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)


# Extend PostViewSet with LikeMixin
class PostViewSet(PostLikeMixin, PostViewSet):
    pass
