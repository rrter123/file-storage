from account.views import UserViewSet
from django.contrib import admin
from django.urls import include, path
from file.views import DownloadByFileViewSet, DownloadByUserViewSet, FileViewSet
from organization.views import OrganizationViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"files", FileViewSet, basename="file")
router.register(r"organizations", OrganizationViewSet, basename="organization")
router.register(
    r"downloadsByUser/(?P<user_id>\d+)",
    DownloadByUserViewSet,
    basename="downloadsByUser",
)
router.register(
    r"downloadsByFile/(?P<file_id>\d+)",
    DownloadByFileViewSet,
    basename="downloadsByFile",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
]
