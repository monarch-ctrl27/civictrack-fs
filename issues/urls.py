from django.urls import path

from . import views

app_name = "issues"

urlpatterns = [
    path("", views.home, name="home"),
    path("report/", views.report_create, name="report_create"),
    path("map/", views.map_feed, name="map_feed"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("role/", views.set_role, name="set_role"),
    path("report/<int:pk>/vote/", views.vote, name="vote"),
    path("report/<int:pk>/comment/", views.comment_add, name="comment_add"),
    path("report/<int:pk>/status/", views.status_update, name="status_update"),
]
