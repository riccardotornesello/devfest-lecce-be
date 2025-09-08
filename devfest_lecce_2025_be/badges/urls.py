from django.urls import path

from .views import BadgeCategoryListView, BadgeListView, ScanBadgeView

urlpatterns = [
    path("", BadgeListView.as_view(), name="badge-list"),
    path("@scan/", ScanBadgeView.as_view(), name="scan-badge"),
    path("@categories/", BadgeCategoryListView.as_view(), name="badge-category-list"),
]
