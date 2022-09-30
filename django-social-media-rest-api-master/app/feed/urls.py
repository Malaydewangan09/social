from django.urls import path
from .views import (FeedView,
                    PostsView,
                    PostsFollowersView,
                    PostsFolloweesView,
                    PostsFriendsView)

urlpatterns = [
    path('', FeedView.as_view(), name='feed-view'),
    path('followers/', PostsFollowersView.as_view(), name='followers-posts-view'),
    path('followees/', PostsFolloweesView.as_view(), name='followees-posts-view'),
    path('friends/', PostsFriendsView.as_view(), name='friends-posts-view'),
    path('<author_id>/', PostsView.as_view(), name='user-posts-view'),

]