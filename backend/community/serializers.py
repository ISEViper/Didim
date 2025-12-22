from rest_framework import serializers
from .models import Post, Comment


class AuthorSerializer(serializers.Serializer):
    """작성자 정보 (간단히)"""
    pk = serializers.IntegerField()
    nickname = serializers.CharField()
    profile_image_url = serializers.SerializerMethodField()
    display_initial = serializers.SerializerMethodField()

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def get_display_initial(self, obj):
        return obj.get_display_initial()


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""
    author = AuthorSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'is_owner']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_is_owner(self, obj):
        """현재 사용자가 작성자인지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록 시리얼라이저"""
    author = AuthorSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'created_at', 'updated_at',
            'like_count', 'comment_count', 'is_liked', 'is_owner'
        ]

    def get_is_liked(self, obj):
        """현재 사용자가 좋아요 했는지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False

    def get_is_owner(self, obj):
        """현재 사용자가 작성자인지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False


class PostDetailSerializer(PostListSerializer):
    """게시글 상세 시리얼라이저 (댓글 포함)"""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['comments']


class PostCreateSerializer(serializers.ModelSerializer):
    """게시글 작성 시리얼라이저"""
    class Meta:
        model = Post
        fields = ['content']