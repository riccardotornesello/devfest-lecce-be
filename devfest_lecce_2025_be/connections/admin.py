from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Connection


class ConnectionResource(resources.ModelResource):
    class Meta:
        model = Connection


class ConnectionAdmin(ImportExportModelAdmin):
    resource_classes = [ConnectionResource]


admin.site.register(Connection, ConnectionAdmin)
