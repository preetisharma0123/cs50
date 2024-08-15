
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("all_posts/<str:username>", views.all_posts, name="all_posts_with_username"),
    path("all_posts/<int:post_id>", views.post, name="post"),
    path("all_posts/<int:post_id>/comments", views.post_comments, name="comments"),
    path("all_posts/<int:post_id>/like", views.post_like, name="comments"),
    path("profile_page/<str:username>", views.profile_page, name="profile_page"),
    path('trending_hashtags', views.trending_hashtags, name='trending_hashtags'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
