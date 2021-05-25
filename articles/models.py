from datetime import datetime
from profiles.models import Profile
from django.db import models

from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class TimestamModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        ordering =['-created_at', '-updated_at']


class Article(TimestamModel):

    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    body = models.TextField()
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    likes = models.ManyToManyField('authentication.User', related_name='likes', blank=True)
    dislikes = models.ManyToManyField('authentication.User', related_name="dislikes", blank=True)
    tags = models.ManyToManyField('articles.Tag', related_name='articles')
    

    def __str__(self):
        return self.title

class Comment(MPTTModel, TimestamModel):

    body = models.TextField()
    comment_likes = models.ManyToManyField('authentication.User', related_name='comment_likes', blank=True)
    comment_dislikes = models.ManyToManyField(
        'authentication.User', 
        related_name='comment_dislikes', 
        blank=True
    )
    parent = TreeForeignKey(
        'self', 
        related_name='reply_set', 
        null=True, 
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        'articles.Article',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'profiles.Profile',
        related_name='comments',on_delete=models.CASCADE
    )


class CommentEditHistory(models.Model):

    body = models.TextField(null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(TimestamModel):

    rater = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    counter = models.IntegerField(default=0)
    stars = models.IntegerField(null=True)


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag 

class Bookmarks(models.Model):

    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='bookmarked', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)

