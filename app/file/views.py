from django.db.models.aggregates import Count
from django.shortcuts import redirect
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from file.models import Download, File
from file.serializers import (
    DownloadByFileSerializer,
    DownloadByUserSerializer,
    FileSerializer,
)


class FileViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = File.objects.annotate(download_count=Count("downloads"))
    serializer_class = FileSerializer

    @action(detail=True)
    def download(self, request, pk=None):
        file = self.get_object()
        Download.objects.create(file=file, user=self.request.user)
        return redirect(file.file_object.url)


class DownloadByUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Download
    serializer_class = DownloadByUserSerializer

    def get_queryset(self):
        if user_id := self.kwargs.get("user_id"):
            return Download.objects.filter(user=user_id)
        return Download.objects.none()


class DownloadByFileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Download
    serializer_class = DownloadByFileSerializer

    def get_queryset(self):
        if file_id := self.kwargs.get("file_id"):
            return Download.objects.filter(file=file_id)
        return Download.objects.none()
