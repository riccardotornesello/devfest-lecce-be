from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    search_fields = ["id", "name", "surname", "linked_in", "instagram"]


admin.site.register(User, UserAdmin)
