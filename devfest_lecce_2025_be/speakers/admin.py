from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Speaker


class SpeakerResource(resources.ModelResource):
    class Meta:
        model = Speaker


class SpeakerAdmin(ImportExportModelAdmin):
    resource_classes = [SpeakerResource]


admin.site.register(Speaker, SpeakerAdmin)
