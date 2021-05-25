import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.renderers import ProfileJSONRenderer, FollowersJSONRenderer, FollowingJSONRenderer
from profiles.serializers import ProfileSerializer
from profiles.exceptions import ProfileDoesNotExist

class ProfileRetrieveAPIView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')

    def retrieve(self, request, username, *args, **kwargs):

        try:
            profile = self.queryset.get(user__username=username)

        except Profile.DoesNotExist:
            raise ProfileDoesNotExist(
                'A profile for {} does not exist.'.format(username)
            )
        
        serializer = self.serializer_class(profile,)

        return Response(serializer.data, status=status.HTTP_200_OK)


