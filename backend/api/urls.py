from django.urls import path
from . import views
from .views import user_manager
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # AUTH (Авторизация)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # USERS (Пайдаланушылар)
    path('users/', views.user_manager, name='user-list'),
    path('users/<int:pk>/', views.user_manager, name='user-detail'),

    # POSTS (Жазбалар)
    path('posts/', views.post_manager, name='post-list'),
    path('posts/<int:pk>/', views.post_manager, name='post-detail'),

    # MEDIA (Суреттер)
    path('posts/<int:post_id>/media/', views.add_media, name='add_media'),

    # INTERACTIONS (Лайктар мен Пікірлер)
    path('posts/<int:post_id>/like/', views.post_interaction, name='post-like'),
    path('posts/<int:post_id>/comments/', views.post_interaction, name='post-comments'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', views.post_interaction, name='comment-detail'),

    # FOLLOWS (Жазылулар)
    path('users/<int:pk>/follow/', views.user_follow, name='user-follow'),
]