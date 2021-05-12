from datetime import datetime, date

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from authentication.renderers import UserJSONRenderer
from authentication.models import User
from authentication.serializers import RegistrationSerializer
from authentication.verification import SendEmail

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_class = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        SendEmail().send_verification_email(user.get('user', None), request)

        return Response(serializer.data, status=HTTP_201_CREATED)



