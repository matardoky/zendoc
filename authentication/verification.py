from six import text_type
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from django.utils.encoding import force_text, force_bytes
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.models import User
from datetime import date

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = TokenGenerator()


class SendEmail():
    def send_verification_email(self, email, request):
        user = User.objects.filter(email=email).first()
        subject = "Verify you Authors Haven account"

        token = account_activation_token.make_token(user)
        current_site = get_current_site(request)

        body = render_to_string('mail.html', context={
            'action_url':"http://",
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':token
        })

        mail = EmailMessage(subject, body, "matar@gmail.com", to=[email])
        mail.content_subtype = 'html'
        mail.send()

        return (token, urlsafe_base64_encode(force_bytes(user.pk)))
