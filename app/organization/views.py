from django.db.models import Count
from rest_framework import serializers, viewsets

from organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    download_count = serializers.CharField(read_only=True)

    class Meta:
        model = Organization
        fields = ("id", "name", "download_count")


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.annotate(download_count=Count("files__downloads"))
    serializer_class = OrganizationSerializer
