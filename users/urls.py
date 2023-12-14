from django.urls import path
from . import views

app_name = "users"

# .com/add_study_spot

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("logout", views.logout_view),
    path("add_study_spot", views.StudySpotCreateView.as_view(), name="add_study_spot"),
    path("map", views.MapView.as_view(), name="map"),
    path("approve_spots", views.StudySpotApproveView.as_view(), name="approve_spots"),
    path("spot/<int:pk>", views.SoloStudySpotView.as_view(), name="spot"),
    path("study_spots", views.StudySpotAggregateView.as_view(), name="study_spots"),
]
