from rest_framework import serializers
from ..models import Blog, Comment





class BlogSerializer(serializers.ModelSerializer):
    blogger = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['pk', 'blogger', 'blog_title', 'post_image', 'blog_post', 'likes', 'comments', 'slug', 'publish_date']

    def get_blogger(self, obj):
        return obj.blogger.username
    
    def get_likes(self, obj):
        return obj.get_likes()
    
    def get_comments(self, obj):
        return obj.get_total_comments()





class SingleBlogCommentSerializer(serializers.ModelSerializer):
    commentor = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['pk', 'commentor', 'comment', 'comment_date', 'likes', 'liked']

    def get_commentor(self, obj):
        return obj.commentor.username

    def get_likes(self, obj):
        return obj.get_likes()

    def get_liked(self, obj):
        return True if self.context['request'].user in obj.get_likers() else False





class SingleBlogSerializer(serializers.ModelSerializer):
    blogger = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    blog_comment = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['pk', 'blogger', 'blog_title', 'post_image', 'blog_post', 'likes', 'total_comments', 'blog_comment', 'slug', 'publish_date', 'liked']

    def get_blogger(self, obj):
        return obj.blogger.username

    def get_liked(self, obj):
        return True if self.context['request'].user in obj.get_likers() else False
    
    def get_likes(self, obj):
        return obj.get_likes()

    def get_total_comments(self, obj):
        return obj.get_total_comments()

    def get_blog_comment(self, obj):
        comments = obj.blog_comment.all()
        serialize = SingleBlogCommentSerializer(instance= comments, data=[], context={'request': self.context['request']}, many=True)
        if serialize.is_valid():
            return serialize.data
        return serialize.errors





class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'blog', 'commentor', 'comment']
        extra_kwargs = {
            'blog': {'required': False},
            'commentor': {'required': False},
        }