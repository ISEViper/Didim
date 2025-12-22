from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    CommentSerializer
)


class PostListCreateView(APIView):
    """게시글 목록 조회 / 작성"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """게시글 목록 조회"""
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """게시글 작성"""
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            # 작성 후 상세 정보 반환
            post = Post.objects.get(pk=serializer.instance.pk)
            return Response(
                PostListSerializer(post, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """게시글 상세 조회 / 수정 / 삭제"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """게시글 상세 조회"""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        """게시글 수정"""
        post = get_object_or_404(Post, pk=pk)
        
        # 작성자만 수정 가능
        if post.author != request.user:
            return Response(
                {'error': '본인이 작성한 글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                PostDetailSerializer(post, context={'request': request}).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """게시글 삭제"""
        post = get_object_or_404(Post, pk=pk)
        
        # 작성자만 삭제 가능
        if post.author != request.user:
            return Response(
                {'error': '본인이 작성한 글만 삭제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    """게시글 좋아요 토글"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """좋아요 추가/취소"""
        post = get_object_or_404(Post, pk=pk)
        
        if post.likes.filter(pk=request.user.pk).exists():
            # 이미 좋아요 했으면 취소
            post.likes.remove(request.user)
            is_liked = False
        else:
            # 좋아요 추가
            post.likes.add(request.user)
            is_liked = True

        return Response({
            'is_liked': is_liked,
            'like_count': post.like_count
        })


class CommentListCreateView(APIView):
    """댓글 목록 조회 / 작성"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_pk):
        """댓글 목록 조회"""
        post = get_object_or_404(Post, pk=post_pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, post_pk):
        """댓글 작성"""
        post = get_object_or_404(Post, pk=post_pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    """댓글 수정 / 삭제"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_pk, pk):
        """댓글 수정"""
        comment = get_object_or_404(Comment, pk=pk, post_id=post_pk)
        
        if comment.author != request.user:
            return Response(
                {'error': '본인이 작성한 댓글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, pk):
        """댓글 삭제"""
        comment = get_object_or_404(Comment, pk=pk, post_id=post_pk)
        
        if comment.author != request.user:
            return Response(
                {'error': '본인이 작성한 댓글만 삭제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)