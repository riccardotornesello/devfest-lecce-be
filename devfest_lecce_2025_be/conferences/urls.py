from django.urls import path

from .views import ConferenceListView

urlpatterns = [
    path("", ConferenceListView.as_view(), name="conference-list"),
]
