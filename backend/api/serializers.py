from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Media, Like, Comment, Follow, Note, Story

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Өрістер Android-тан келмесе де қате бермеуі үшін default мән береміз
    email = serializers.EmailField(required=False, allow_null=True, default="")
    bio = serializers.CharField(required=False, allow_blank=True, default="")
    avatar_url = serializers.CharField(required=False, allow_blank=True, default="")
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'avatar_url']

    def create(self, validated_data):
        # Парольді ашық күйінде емес, хэштеп сақтау үшін create_user маңызды
        user = User.objects.create_user(**validated_data)
        return user

# Қалған MediaSerializer, PostSerializer және т.б. өзгеріссіз қала береді

# 2. Media Serializer
class MediaSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'mime_type', 'width', 'height', 'order_idx']

# 3. Note Serializer
class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Note
        fields = ['id', 'user', 'text', 'created_at']

# 4. Story Serializer
class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Story
        fields = ['id', 'user', 'file', 'created_at']

# 5. Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 
    media = MediaSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_at', 'media']

# 6. Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

# 7. Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at']

# 8. Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'