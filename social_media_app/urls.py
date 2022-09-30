from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register),
    path('authenticate/', authenticate),
    path('user/', user),
    path('posts/<int:post_id>', posts),
    path('posts/', create_post),
    path('all_posts/', all_posts),
    path('follow/<int:following_to_id>', follow),
    path('unfollow/<int:following_to_id>', unfollow),
    path('like/<int:post_id>', like),
    path('unlike/<int:post_id>', unlike),
    path('comment/<int:post_id>', comment),
]
