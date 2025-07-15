from django.contrib import admin

from .models import Conference, ConferenceTopic, ConferenceType

admin.site.register(Conference)
admin.site.register(ConferenceTopic)
admin.site.register(ConferenceType)
