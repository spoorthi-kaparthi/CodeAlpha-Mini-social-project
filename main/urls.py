from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("users/", views.users, name="users"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
]