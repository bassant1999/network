
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makePost", views.makePost, name="makePost"),
    path("profile/<int:uid>", views.profile, name="profile"),
    path("like/<int:pid>", views.like, name="like"),
    path("follow/<int:uid>", views.follow, name="follow"),
    path("unfollow/<int:uid>", views.unfollow, name="unfollow"),
    path("edit", views.edit, name="edit"),
    path("following", views.following, name="following"),
    
    
]
