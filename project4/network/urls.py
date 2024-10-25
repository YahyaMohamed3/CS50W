
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post" , views.post , name="post"),
    path("profile/<str:username>" , views.profile, name="profile"),
    path("posts" , views.following_posts , name="following_posts"),
    path("post/<int:postId>/like" , views.toggle_like, name="like"),
    path("post/<int:postId>/edit", views.edit , name="edit")
]
