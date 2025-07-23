from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("badges/", include("badges.urls")),
    path("conferences/", include("conferences.urls")),
]
