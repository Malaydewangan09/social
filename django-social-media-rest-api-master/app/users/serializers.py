from rest_framework import serializers
from app_api.models import UserProfile, Friendship, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "avatar"


class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = '__all__'

    def validate_request(self, receiver, sender):
        """
        check that sender is different from receiver
        """
        if sender == receiver:
            raise serializers.ValidationError("Invalid friendship")


class FriendRequestSerializer(serializers.ModelSerializer):

    sender = UserSerializer(
        read_only=True,
    )
    receiver = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Friendship
        fields = ['sender', 'receiver', 'status']
        read_only_fields = fields


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class FollowLightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['status']
