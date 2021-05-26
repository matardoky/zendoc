import re

from notifications.models import Notification
from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from articles.models import Article, Bookmarks, Comment, Rating, Tag, CommentEditHistory
from articles.tag_relations import TagRelatedField

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    reply_set = RecursiveSerializer(many=True, read_only=True)
    comment_likes = serializers.SerializerMethodField()
    comment_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 
            'author', 
            'comment_likes',
            'comment_dislikes',
            'body',
            'reply_set', 
            'created_at', 
            'updated_at',
        ]

    def create(self, validated_data):
        article = self.context['article']
        author = self.context['author']
        parent = self.context.get('parent', None)

        return Comment.objects.create(
            author=author, article=article, parent=parent, **validated_data
        )
    
    def get_comment_likes(self, obj):
        return obj.comment_likes.count()

    def get_comment_dislikes(self, obj):
        return obj.comment_dislikes.count()

    def is_edited(self):
        return False

    
class ArticleSerialzer(serializers.ModelSerializer):

    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    slug = serializers.SlugField(required=False)
    image_url = serializers.URLField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    author = ProfileSerializer(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(required=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')
    favorited = serializers.SerializerMethodField(
        method_name='is_favorited'
    )
    favoriteCount = serializers.SerializerMethodField(
        method_name='get_favoite_count'
    )
    bookmarked = serializers.SerializerMethodField(
        method_name='is_bookmarked'
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'body', 'comments',
            'description', 'image_url', 'created_at', 'updated_at',
            'author', 'average_rating', 'likes', 'dislikes', 'dislikes_count',
            'likes_count', 'tagList', 'favorited', 'favoriteCount', 'bookmarked'
        ]

    def get_favorite_count(self, instance):
        return instance.users_fav_articles.count()

    def is_favorited(self, instance):
        request = self.context.get('request')
        if request is None:
            return False
        username = request.user.username
        if instance.users_fav_articles.filter(user__username=username).count() == 0:
            return False
        return True

    def is_bookmarked(self, instance):
        request = self.context.get('request')
        if request is None:
            return False
        if Bookmarks.objects.filter(article_id=instance.id, user_id=instance.author.user_id):
            return True

        return False

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    def validate(self, data):
        pass

    def create(self, validated_data):

        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)

        for tag in tags:
            article.tags.add(tag)
        return article