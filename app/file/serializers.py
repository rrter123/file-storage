from rest_framework import serializers
from rest_framework.reverse import reverse

from file.models import Download, File


class FileSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)
    download_link = serializers.SerializerMethodField()
    download_count = serializers.IntegerField(read_only=True)

    def get_download_link(self, file):
        request = self.context["request"]
        return reverse("file-download", kwargs={"pk": file.id}, request=request)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["file_object"] = instance.filename
        return data

    def create(self, validated_data):
        validated_data["organization"] = self.context[
            "request"
        ].user.employee.organization
        return super().create(validated_data)

    class Meta:
        model = File
        fields = (
            "id",
            "organization",
            "file_object",
            "download_link",
            "download_count",
        )


class DownloadByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ("id", "file", "download_time")


class DownloadByFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ("id", "user", "download_time")
