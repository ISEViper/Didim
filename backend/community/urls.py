from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    PostLikeView,
    CommentListCreateView,
    CommentDetailView
)

app_name = 'community'

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]