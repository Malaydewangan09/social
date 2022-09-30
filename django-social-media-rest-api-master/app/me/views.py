from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import MeSerializer

User = get_user_model()


class GetUpdateUserProfileView(GenericAPIView):
    serializer_class = MeSerializer

    def get(self, request):
        return Response(self.get_serializer(request.user).data)

    def post(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.get_serializer(user).data)

