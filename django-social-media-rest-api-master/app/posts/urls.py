from django.urls import path
from .views import (PostRetrieveUpdateDestroyView,
                    PostCreateAPIView,
                    PostsLikedAPIView,
                    PostLikeAPIView)

urlpatterns = [
    path('liked/', PostsLikedAPIView.as_view(), name='liked-posts'),
    path('new-post/', PostCreateAPIView.as_view(), name='post-new'),
    path('<pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-delete'),
    path('like/<post_id>', PostLikeAPIView.as_view(), name='like-unlike-post'),
]

