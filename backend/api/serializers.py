from rest_framework import serializers
from .models import User, Post, Media, Like, Comment, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar_url']

class MediaSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'mime_type', 'width', 'height', 'order_idx']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 
    media = MediaSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_at', 'media']

# Қате шығып тұрған жері — осы класстардың жоқтығы:
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # post пен author өрістерін read_only қыламыз
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'