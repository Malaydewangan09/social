from rest_framework import serializers
from app_api.models import Post


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
