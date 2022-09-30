from rest_framework import serializers
from app_api.models import Post, Reaction


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):

    posts = PostSerializer(many=False)

    class Meta:
        model = Reaction
        fields = '__all__'


class ReactionLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['status']
