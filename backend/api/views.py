from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
# Жаңа моделдер қосылды: Note, Story
from .models import User, Post, Media, Like, Comment, Follow, Note, Story 
# Жаңа серилизаторлар қосылды: NoteSerializer, StorySerializer
from .serializers import (
    UserSerializer, PostSerializer, MediaSerializer, 
    LikeSerializer, CommentSerializer, FollowSerializer,
    NoteSerializer, StorySerializer
)

# --    - СІЗДІҢ БҰРЫНҒЫ ЛОГИКАҢЫЗ (ӨЗГЕРІССІЗ) ---

# 1. USERS
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([AllowAny]) # Тіркелуге бәріне рұқсат
def user_manager(request, pk=None):
    if request.method == 'GET':
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # ЕГЕР 400 ҚАТЕСІ ШЫҚСА, МЫНА ЖОЛДАР ТЕРМИНАЛҒА СЕБЕБІН ШЫҒАРАДЫ:
        print("--- VALIDATION ERROR ---")
        print(serializer.errors)
        print("------------------------")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "Юзер өшірілді"}, status=status.HTTP_204_NO_CONTENT)
# 2. POSTS
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_manager(request, pk=None):
    if request.method == 'GET':
        if pk:
            post = get_object_or_404(Post, pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            posts = Post.objects.all().order_by('-created_at')
            paginator = PageNumberPagination()
            page = paginator.paginate_queryset(posts, request)
            if page is not None:
                serializer = PostSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            raise PermissionDenied("Бұл сіздің постыңыз емес!")
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            raise PermissionDenied("Бұл сіздің постыңыз емес!")
        post.delete()
        return Response({"message": "Пост өшірілді"}, status=status.HTTP_204_NO_CONTENT)

# 3. COMMENTS & LIKES
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_interaction(request, post_id, comment_id=None):
    post = get_object_or_404(Post, pk=post_id)
    if 'like' in request.path:
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created: return Response({"message": "Лайк басылды"}, status=201)
            return Response({"message": "Сіз бұл постқа лайк басып қойғансыз"}, status=200)
        elif request.method == 'DELETE':
            like = Like.objects.filter(user=request.user, post=post)
            if like.exists():
                like.delete()
                return Response({"message": "Лайк өшірілді"}, status=204)
            return Response({"error": "Лайк табылған жоқ"}, status=404)
    if 'comment' in request.path:
        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=201)
        elif request.method == 'PUT':
            comment = get_object_or_404(Comment, pk=comment_id, post=post)
            if comment.author != request.user: raise PermissionDenied("Бұл сіздің пікіріңіз емес")
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        elif request.method == 'DELETE':
            comment = get_object_or_404(Comment, pk=comment_id, post=post)
            if comment.author == request.user or post.author == request.user:
                comment.delete()
                return Response({"message": "Пікір өшірілді"}, status=204)
            raise PermissionDenied("Өшіруге рұқсат жоқ")
    return Response({"error": "URL қате"}, status=405)

# 4. FOLLOWS
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        followers = Follow.objects.filter(followee=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user == user: raise ValidationError("Өзіңізге жазыла алмайсыз")
        Follow.objects.get_or_create(follower=request.user, followee=user)
        return Response({"message": "Жазылдыңыз"}, status=201)
    elif request.method == 'DELETE':
        Follow.objects.filter(follower=request.user, followee=user).delete()
        return Response({"message": "Жазылудан бас тарттыңыз"}, status=204)
    return Response({"error": "Method not allowed"}, status=405)

# 5. MEDIA
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_media(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user: raise PermissionDenied("Бұл сіздің постыңыз емес!")
    serializer = MediaSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- ЖАҢАДАН ҚОСЫЛҒАН БӨЛІМДЕР ---

# 6. NOTES (Заметкалар)
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_manager(request):
    # 24 сағаттық шектеу
    time_threshold = timezone.now() - timedelta(hours=24)

    if request.method == 'GET':
        notes = Note.objects.filter(created_at__gte=time_threshold).order_by('-created_at')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Инстаграм сияқты: жаңа заметка жазса, ескісі өшеді
        Note.objects.filter(user=request.user).delete()
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        Note.objects.filter(user=request.user).delete()
        return Response({"message": "Заметка өшірілді"}, status=status.HTTP_204_NO_CONTENT)

# 7. STORIES (Историялар)
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def story_manager(request, pk=None):
    time_threshold = timezone.now() - timedelta(hours=24)

    if request.method == 'GET':
        stories = Story.objects.filter(created_at__gte=time_threshold).order_by('-created_at')
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        story = get_object_or_404(Story, pk=pk, user=request.user)
        story.delete()
        return Response({"message": "История өшірілді"}, status=status.HTTP_204_NO_CONTENT)