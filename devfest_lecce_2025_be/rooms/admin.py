from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Room


class RoomResource(resources.ModelResource):
    class Meta:
        model = Room


class RoomAdmin(ImportExportModelAdmin):
    resource_classes = [RoomResource]


admin.site.register(Room, RoomAdmin)
