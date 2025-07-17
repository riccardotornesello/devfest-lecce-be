from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Conference, ConferenceTopic, ConferenceType


class ConferenceResource(resources.ModelResource):
    class Meta:
        model = Conference


class ConferenceTopicResource(resources.ModelResource):
    class Meta:
        model = ConferenceTopic


class ConferenceTypeResource(resources.ModelResource):
    class Meta:
        model = ConferenceType


class ConferenceAdmin(ImportExportModelAdmin):
    resource_classes = [ConferenceResource]


class ConferenceTopicAdmin(ImportExportModelAdmin):
    resource_classes = [ConferenceTopicResource]


class ConferenceTypeAdmin(ImportExportModelAdmin):
    resource_classes = [ConferenceTypeResource]


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(ConferenceTopic, ConferenceTopicAdmin)
admin.site.register(ConferenceType, ConferenceTypeAdmin)
