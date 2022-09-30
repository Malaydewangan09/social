from app_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from django.db.models import Q

from app_api.models import Post, Friendship, Follow
from .serializers import FeedSerializer
from users.serializers import FriendshipSerializer, FollowSerializer
from posts.serializers import PostSerializer


class FeedView(generics.ListAPIView):
    """
    Class to get all the Posts of the Feed Application
    """
    queryset = Post.objects.all()
    serializer_class = FeedSerializer


class PostsView(generics.ListAPIView):
    """
    Class to get all Posts of a specific User using
    the ID of the User (author)
    """
    serializer_class = FeedSerializer

    def get_queryset(self, *args, **kwargs):
        kwargs = self.kwargs  # --> a dictionary with the url's parameter {'author_id': '2'}
        kw_id = kwargs.get('author_id')  # --> returns the value of key='author_id'
        return Post.objects.filter(author_id=kw_id)


class PostsFollowersView(generics.ListAPIView):
    """
    Class to get all the Posts of followers
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        # get the followers of the loged-in user --> request.user
        followers = Follow.objects.filter(Q(receiver=self.request.user) & Q(status='Follow'))
        # serialize the data
        serializer = FollowSerializer(followers, many=True)
        # create a list with their id's
        sender_id = [friend['sender'] for friend in serializer.data]

        # query --> SELECT * FROM post WHERE author IN sender_id
        queryset = Post.objects.filter(Q(author__in=sender_id))

        return queryset


class PostsFolloweesView(generics.ListAPIView):
    """
    Class to get all the Posts of followees
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        # get the followers of the loged-in user --> request.user
        followers = Follow.objects.filter(Q(sender=self.request.user) & Q(status='Follow'))
        # serialize the data
        serializer = FollowSerializer(followers, many=True)
        # create a list with their id's
        receiver_id = [friend['receiver'] for friend in serializer.data]

        # query --> SELECT * FROM post WHERE author IN sender_id
        queryset = Post.objects.filter(Q(author__in=receiver_id))

        return queryset


class PostsFriendsView(generics.ListAPIView):
    """
    Class to get all the Posts of friends
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        # get the user_id of the current user
        current_user_id = self.request.user.id
        # get the friends of the loged-in user --> request.user
        friends = Friendship.objects.filter((Q(receiver=self.request.user) & Q(status='Accept'))
                                            | Q(sender=self.request.user) & Q(status='Accept'))

        # serialize the data
        serializer = FriendshipSerializer(friends, many=True)
        # create a list with their id's
        sender_id = [friend['sender'] for friend in serializer.data if friend['sender'] != current_user_id]
        receiver_id = [friend['receiver'] for friend in serializer.data if friend['receiver'] != current_user_id]

        # query --> SELECT * FROM post WHERE author IN (sender_id or receiver_id)
        queryset = Post.objects.filter(Q(author__in=sender_id) | Q(author__in=receiver_id))

        return queryset
