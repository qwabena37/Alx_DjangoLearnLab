from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    post_id = serializers.PrimaryKeyRelatedField(source='post', queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post_id',    # write-only relation input (post primary key)
            'post',       # will be serialized as PK by DRF by default if requested
            'author',
            'author_id',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at', 'post']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # include post id explicitly for convenience
        rep['post_id'] = instance.post.id
        return rep


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comments',  # nested read-only comments
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at', 'comments']
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post_id = serializers.PrimaryKeyRelatedField(source='post', queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post_id', 'post', 'user', 'user_id', 'created_at']
        read_only_fields = ['id', 'user', 'user_id', 'created_at', 'post']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post_id'] = instance.post.id
        return rep
