from app_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q


from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from app_api.models import UserProfile, Follow, Friendship

from users.serializers import (UserProfileSerializer,
                               UserSerializer,
                               FollowSerializer,
                               FriendshipSerializer,
                               FollowLightSerializer,
                               FriendRequestSerializer)

User = get_user_model()


class UsersView(generics.ListAPIView):
    """
    Class to List all Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserProfilesView(generics.ListAPIView):
    """
    Class to List all Users Profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserProfileView(APIView):
    """
    Class to Retrieve a User Profile using the user_id
    """
    def get_object(self, pk):
        user_profile = get_object_or_404(UserProfile, pk=pk)
        return user_profile

    def get(self, request, pk):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)


class UserFollowView(APIView):
    """
    Class to Follow / Unfollow a User using the user_id
    """

    serializer_class = FollowLightSerializer

    def get_user(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        return user

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        if request.user != self.get_user(user_id):
            Follow.objects.get_or_create(sender=request.user, receiver=self.get_user(user_id), status='Follow')
            return Response({"Status 201": "Follow Successful"}, status=status.HTTP_201_CREATED)
        return Response({"Status 404": "Sender must be different than receiver"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        if request.user != self.get_user(user_id):
            Follow.objects.filter(Q(sender=request.user) & Q(receiver=user_id)).delete()
            return Response({"Status 204": "Unfollow Successful"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"Status 404": "Sender must be different than receiver"}, status=status.HTTP_400_BAD_REQUEST)


class UserFollowersView(generics.ListAPIView):
    """
    Class to List all User's Followers
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # get the followers of the loged-in user --> request.user
        followers = Follow.objects.filter(Q(receiver=self.request.user) & Q(status='Follow'))
        # serialize the data
        serializer = FollowSerializer(followers, many=True)
        # create a list with their id's
        sender_id = [follower['sender'] for follower in serializer.data]

        # query --> SELECT * FROM post WHERE author IN sender_id
        queryset = UserProfile.objects.filter(Q(id__in=sender_id))

        return queryset


class UserFolloweesView(generics.ListAPIView):
    """
    Class to List all the User's Followees
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # get the followees of the loged-in user --> request.user
        followees = Follow.objects.filter(Q(sender=self.request.user) & Q(status='Follow'))
        # serialize the data
        serializer = FollowSerializer(followees, many=True)
        # create a list with their id's
        receiver_id = [followee['receiver'] for followee in serializer.data]

        # query --> SELECT * FROM post WHERE author IN receiver_id
        queryset = UserProfile.objects.filter(Q(id__in=receiver_id))

        return queryset


class FriendRequestView(APIView):
    """
    Class to send a friend request to a User using the user_id
    """

    serializer_class = FriendRequestSerializer

    def get_user(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        return user

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        if request.user != self.get_user(user_id):
            Friendship.objects.get_or_create(sender=request.user, receiver=self.get_user(user_id), status='Pending')
            return Response({"Status 201": "Friend Request Successful"}, status=status.HTTP_201_CREATED)
        return Response({"Status 404": "Sender must be different than receiver"}, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestsView(generics.ListAPIView):
    """
    Class to view all User's Friend Requests
    """
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print(self)
        # get the friend requests of the loged-in user --> request.user
        friend_requests = Friendship.objects.filter(Q(receiver=self.request.user))

        # if they are pending requests
        if friend_requests.exists():
            # serialize the data
            serializer = FriendshipSerializer(friend_requests, many=True)
            # create a list with their id's
            sender_id = [friend_request['sender'] for friend_request in serializer.data]
            # query --> SELECT * FROM post WHERE author IN sender_id
            queryset = UserProfile.objects.filter(Q(id__in=sender_id))

            return queryset


class FriendRequestsPendingView(generics.ListAPIView):
    """
    Class to view all User's Open (status="Pending') Friend Requests
    """
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print(self)
        # get the friend requests of the loged-in user --> request.user
        friend_requests = Friendship.objects.filter(Q(receiver=self.request.user) & Q(status='Pending'))

        # if they are pending requests
        if friend_requests.exists():
            # serialize the data
            serializer = FriendshipSerializer(friend_requests, many=True)
            # create a list with their id's
            sender_id = [friend_request['sender'] for friend_request in serializer.data]
            # query --> SELECT * FROM post WHERE author IN sender_id
            queryset = UserProfile.objects.filter(Q(id__in=sender_id))

            return queryset


class FriendRequestAcceptView(APIView):
    """
    Class to Accept a Friend Request using the user_id
    """

    serializer_class = FriendshipSerializer

    def get_user(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        return user

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        # Query to check if the user has a pending request
        friend_request = Friendship.objects.filter(Q(receiver=self.request.user)
                                                   & Q(sender=self.get_user(user_id))
                                                   & Q(status='Pending'))

        # If there is a pending request
        if friend_request.exists():
            if request.user != self.get_user(user_id):
                Friendship.objects.get_or_create(receiver=request.user, sender=self.get_user(user_id), status='Accept')
                return Response({"Status 201": "Friend Request Accepted"}, status=status.HTTP_201_CREATED)
            return Response({"Status 404": "Sender must be different than receiver"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status 404": "There is no pending friend request"}, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestRejectView(APIView):
    """
    Class to Reject a Friend Request using the user_id
    """

    serializer_class = FriendshipSerializer

    def get_user(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        return user

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        # Query to check if the user has a pending request
        friend_request = Friendship.objects.filter(Q(receiver=self.request.user)
                                                   & Q(sender=self.get_user(user_id))
                                                   & Q(status='Pending')
                                                   )

        # If there is a pending request
        if friend_request.exists():
            if request.user != self.get_user(user_id):
                Friendship.objects.get_or_create(receiver=request.user, sender=self.get_user(user_id), status='Reject')
                return Response({"Status 201": "Friend Request Rejected"}, status=status.HTTP_201_CREATED)
            return Response({"Status 404": "Sender must be different than receiver"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status 404": "There is no pending friend request"}, status=status.HTTP_400_BAD_REQUEST)


class UserFriendsView(generics.ListAPIView):
    """
    Class to List all User's Friends
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # get the user_id of the current user
        current_user_id = self.request.user.id
        # get the followers of the loged-in user --> request.user
        friends = Friendship.objects.filter((Q(receiver=self.request.user) & Q(status='Accept'))
                                            | Q(sender=self.request.user) & Q(status='Accept'))
        # serialize the data
        serializer = FriendshipSerializer(friends, many=True)
        # create a list with their id's
        sender_id = [friend['sender'] for friend in serializer.data if friend['sender'] != current_user_id]
        receiver_id = [friend['receiver'] for friend in serializer.data if friend['receiver'] != current_user_id]

        # query --> SELECT * FROM post WHERE author IN (sender_id or receiver_id)
        queryset = UserProfile.objects.filter(Q(user__in=sender_id) | Q(user__in=receiver_id))

        return queryset


class UserUnfriendView(APIView):
    """
    Class to Unfriend a User
    """
    serializer_class = FriendshipSerializer

    @staticmethod
    def get_user(user_id):
        user = get_object_or_404(User, pk=user_id)
        return user

    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')

        # Query to check if the users are friends
        is_friends1 = Friendship.objects.filter(Q(receiver=request.user) &
                                      Q(sender=self.get_user(user_id)) &
                                      Q(status='Accept'))
        is_friends2 = Friendship.objects.filter(Q(sender=request.user) &
                                      Q(receiver=self.get_user(user_id)) &
                                      Q(status='Accept'))
        # If they are friends
        if is_friends1.exists() or is_friends2.exists():
            # check who is the receiver
            if request.user != self.get_user(user_id):
                # If current user was the receiver of the friend request
                Friendship.objects.filter(Q(receiver=request.user) &
                                          Q(sender=self.get_user(user_id)) &
                                          Q(status='Accept')).delete()

                # If current user was the sender of the friend request
                Friendship.objects.filter(Q(sender=request.user) &
                                          Q(receiver=self.get_user(user_id)) &
                                          Q(status='Accept')).delete()
                # if they are friends --> unfriend
                return Response({"Status 204": "Unfriend Successful"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"Status 404": "You are not friends!"}, status=status.HTTP_400_BAD_REQUEST)
