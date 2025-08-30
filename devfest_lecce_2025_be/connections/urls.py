from django.urls import path

from .views import ConnectionListView

urlpatterns = [
    path("", ConnectionListView.as_view()),
]
