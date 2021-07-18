from django.db import models
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    image = models.TextField(blank=True)
    interests = models.CharField(max_length=255 ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(
        'articles.Article', 
        symmetrical=False, 
        related_name='user_fav_articles'
    )
    follows = models.ManyToManyField(
        'self', 
        related_name='follower',
        symmetrical=False
    )

    def __str__(self):
        return self.user.email

    def favorite(self, article):
        return self.favorites.add(self.article)

    def unfavorite(self, article):
        return self.favorites.remove(self.article)

    def follow(self, profile):
        return self.follows.add(profile)

    def unfollow(self, profile): 
        return self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    def is_follower(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    

