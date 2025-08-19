from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Badge, BadgeCode, OwnBadge


class BadgeResource(resources.ModelResource):
    class Meta:
        model = Badge


class OwnBadgeResource(resources.ModelResource):
    class Meta:
        model = OwnBadge


class BadgeCodeResource(resources.ModelResource):
    class Meta:
        model = BadgeCode


class BadgeAdmin(ImportExportModelAdmin):
    resource_classes = [BadgeResource]


class OwnBadgeAdmin(ImportExportModelAdmin):
    resource_classes = [OwnBadgeResource]


class BadgeCodeAdmin(ImportExportModelAdmin):
    resource_classes = [BadgeCodeResource]


admin.site.register(Badge, BadgeAdmin)
admin.site.register(OwnBadge, OwnBadgeAdmin)
admin.site.register(BadgeCode, BadgeCodeAdmin)
