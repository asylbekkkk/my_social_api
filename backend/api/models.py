from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# 1. Пайдаланушылар кестесі
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True) 
    bio = models.TextField(null=True, blank=True)
    avatar_url = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# 2. Посттар кестесі
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Медиа файлдар кестесі
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.ImageField(upload_to='post_media/', null=True, blank=True)  
    mime_type = models.CharField(max_length=64)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    order_idx = models.IntegerField(default=0)

# --- ЖАҢАДАН ҚОСЫЛҒАН КЕСТЕЛЕР ---

# 4. Заметки (Notes) - Профильдегі қысқа статус
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.CharField(max_length=60) # Инстаграмдағыдай қысқа мәтін
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        # 24 сағаттан аспағанын тексеру
        return self.created_at >= timezone.now() - timedelta(hours=24)

# 5. История (Stories)
class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    file = models.URLField(max_length=512) # Сурет немесе видео
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Stories"

# --- ЕСКІ КЕСТЕЛЕРДІҢ ЖАЛҒАСЫ ---

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)