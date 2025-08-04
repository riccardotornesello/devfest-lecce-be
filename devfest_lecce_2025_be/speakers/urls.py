from django.urls import path

from .views import SpeakerListView

urlpatterns = [
    path("", SpeakerListView.as_view(), name="speaker-list"),
]
