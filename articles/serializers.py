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