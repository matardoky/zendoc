from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from authentication.models import User

class SendEmail:

    def send_article_notification_email(self, email, title, author):
        user = User.objects.filter(email=email).first()
        subject = "Notifications"

        body = render_to_string('article_notification.html', context={
            'action_url':"http://",
            'user': user,
            'title': title,
            'author': author
        })
        mail = EmailMessage(
            subject, body, "zendoc@gmail.com", to=[email]
        )
        mail.content_subtype = 'html'
        mail.send()

    def send_comment_notification_email(self, email, title, author, commenter):

        user = User.objects.filter(email=email).first()

        subject = "Notifications"

        body = render_to_string('comment_notification.html', context={
            'action_url': 'http://',
            'user': user,
            'title': title, 
            'author': author,
            'commenter': commenter
        })

        mail = EmailMessage(
            subject, body, "zendoc@gmail.com", to=[email]
        )
        mail.content_subtype = 'html'

        mail.send()
