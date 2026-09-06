from django.db.models.aggregates import Count
from django.shortcuts import redirect
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from file.models import Download, File
from file.serializers import FileSerializer


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
