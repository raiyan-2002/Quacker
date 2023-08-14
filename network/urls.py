
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("users/<int:num>", views.user, name="user"),
    path("following", views.following, name="following"),


    # API urls
    path("follow_update/<int:num>", views.update_followers, name="update_followers"),
    path("like_update/<int:num>", views.like_update, name="like_update"),
    path("edit_post/<int:num>/<str:text>", views.edit_post, name="edit_post")

]
