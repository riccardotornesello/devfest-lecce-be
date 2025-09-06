from django.contrib import admin
from django.utils.html import format_html
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
    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(
                    obj.picture.url
                )
            )

    resource_classes = [BadgeResource]
    list_display = ["name", "description", "points", "picture_preview"]
    readonly_fields = ("picture_preview",)


class OwnBadgeAdmin(ImportExportModelAdmin):
    resource_classes = [OwnBadgeResource]


class BadgeCodeAdmin(ImportExportModelAdmin):
    resource_classes = [BadgeCodeResource]


admin.site.register(Badge, BadgeAdmin)
admin.site.register(OwnBadge, OwnBadgeAdmin)
admin.site.register(BadgeCode, BadgeCodeAdmin)
