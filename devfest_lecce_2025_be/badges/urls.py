from django.urls import path

from .views import BadgeListView, ScanBadgeView

urlpatterns = [
    path("", BadgeListView.as_view(), name="badge-list"),
    path("@scan/", ScanBadgeView.as_view(), name="scan-badge"),
]
