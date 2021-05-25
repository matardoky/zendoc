from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from notifications.signals import notify


from articles.models import Article, Comment
from articles.notification_emails import SendEmail
from authentication.models import User


@receiver(pre_save, sender=Article)
def pre_save_article_receiver(sender, instance, *args, **kwargs):

    if instance.slug:
        return instance
    slug = slugify(instance.title)
    num =1
    unique_slug = slug 

    while Article.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%s' % (slug, num)
        num +=1
    
    instance.slug = unique_slug


@receiver(post_save, sender=Article)
def notify_followers_new_articles(sender, instance, created, **kwargs):

    if created:

        user = User.objects.get(pk=instance.author.user.id)
        title = instance.title
        author = instance.author.user.get_full_name()
        recipients = []
    
        for follower in user.profile.follower.all():
            if follower.user.get_notified:
                recipients.append(follower.user)
            SendEmail().send_article_notification_email(
                follower.user.email, title, author
            )
        notify.send(instance, recipients=recipients, verb='was posted', slug=instance.slug,
            title = instance.title, author=instance.author.user.get_full_name()
        )


@receiver(post_save, sender=Comment)
def notify_comments_favorited_articles(sender, instance, created, **kwargs):

    if created:
        
        users = instance.article.users_fav_articles.all()
        title = instance.article.title
        slug = instance.article.slug
        author = instance.article.author.user.get_full_name()
        commenter = instance.author.user.get_full_name()
        comment = instance.body
    
        recipients = []
        for user in users:
            if user.user.get_notified:
                recipients.append(user.user)
            SendEmail().send_comment_notification_email(
                user.user.email, title, author, commenter
            )
        
        notify.send(instance, recipients=recipients, verb='was commented on', 
            slug=slug, title=title, author=author,commenter=commenter, comment=comment
        )


