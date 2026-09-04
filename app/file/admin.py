from django.contrib import admin

from file.models import Download, File


class DownloadAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Download, DownloadAdmin)
admin.site.register(File, FileAdmin)
