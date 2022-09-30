from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import (RegistrationSerializer,
                          RegistrationValidationSerializer)


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save(serializer.validated_data)
        return Response(self.get_serializer(new_user).data)


class RegistrationValidationView(GenericAPIView):
    serializer_class = RegistrationValidationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            serializer.validated_data,
        )
        return Response(self.get_serializer(user).data)
