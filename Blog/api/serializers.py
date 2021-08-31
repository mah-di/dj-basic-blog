from rest_framework import serializers
from ..models import Blog


class BlogSerializer(serializers.ModelSerializer):
    blogger = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['blogger', 'blog_title', 'post_image', 'blog_post', 'likes', 'slug', 'publish_date', 'liked']

    def get_blogger(self, obj):
        return obj.blogger.username

    def get_liked(self, obj):
        return True if self.context['request'].user in obj.get_likers() else False
    
    def get_likes(self, obj):
        return obj.get_likes()