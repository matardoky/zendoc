import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class JWTAuthentication(BaseAuthentication): 
    authentication_header_prefix = "Token"

    def authenticate(self, resquest): 

        request.user = None
        auth_header = get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() ! == auth_header_prefix:
            return None

        return self._authenication_credentials(request, token)

    
    def _authentication_credentials(self, request, token):

        try:
            payload = jwt.decode(token, settings.dev.SECRET_KEY)
        except:
            msg="Invalid authentication. Could not decode token"
            raise AuthenticationFailed(msg)
        
        try:
            user = User.objects.get(pk=payload["id"])
        except:
            msg="No user matching this token was found"
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg="This user has been deactivated"
            raise AuthenticationFailed(msg)

        if not user.is_verified:
            msg="This user has not been verified"
            raise AuthenticationFailed(msg)

        return (user, token)




