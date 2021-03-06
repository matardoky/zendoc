from datetime import datetime, date
import logging

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http.response import HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from authentication.renderers import UserJSONRenderer
from authentication.models import User
from authentication.serializers import (
    RegistrationSerializer, LoginSerializer, PasswordResetSerializer,
    UserSerializer

)
from authentication.verification import SendEmail, account_activation_token

logger = logging.getLogger(__name__)

class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes =[UserJSONRenderer]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get("user", {})

        logger.info(
            "USER",
            user.get("email", None)
        )

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        SendEmail().send_verification_email(user.get('email', None), request)

        return Response(serializer.data, status=HTTP_201_CREATED)


class Activate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            return HttpResponse('Thank you for your email confirmation. Now you can login your account')
        else:
            return HttpResponse('Activation link is invalid !')


class LoginAPIView(APIView):

    permission_classes=(AllowAny,)
    renderer_classes=(UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):

        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=HTTP_200_OK)


class PasswordResetAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes=(UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        if not serializer.data["email"] == 'False':
            SendEmail().send_password_reset_email(user.get("email"), request)
            return Response({"msg":"Success, reset email send"}, status=HTTP_200_OK)
        
        return Response({"msg":"Email doesn't exist, register instead"}, status=HTTP_404_NOT_FOUND)


class Reset(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_reset = True
            user.save()

            encode_email = urlsafe_base64_encode(force_bytes(user.email))

            return Response({"token": encode_email})
        else:
            Response({"msg":"Error"})

class PasswordResetConfirmAPIView(APIView):

    def post(self, request):
        pass


    






