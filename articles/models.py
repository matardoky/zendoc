from django.db import models


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


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag 

