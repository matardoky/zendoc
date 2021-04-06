from rest_framework.permissions import IsAuthenticated, IsAdminUser


class EventMixin(object):
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator= self.request.user)