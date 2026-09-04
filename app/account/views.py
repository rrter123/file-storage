from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_staff", "is_superuser")


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
