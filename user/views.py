from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from user.Serializers.register_serializer import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Successfully registered."}, status=status.HTTP_201_CREATED
        )
