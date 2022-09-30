from app_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.db.models import Q

from app_api.models import Post, Reaction
from posts.serializers import PostSerializer, ReactionSerializer, ReactionLikeSerializer


class PostCreateAPIView(APIView):
    """
    Class to create a Post for the Post Application
    """

    def get(self, request):
        post = Post.objects.first()
        serializer = PostSerializer(post)
        return Response({"This is a typical Json post": {"required": "title, body, author"}, "data": serializer.data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Post created succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyView(APIView):
    """
    Class to
     Retrieve / Update / Delete a Post by Post ID
    """

    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Post Updated succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status 201": "Post updated succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response({"Status 204": "Post deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)


class PostLikeAPIView(APIView):
    """
    Class to like and unlike a Post using the post_id
    """
    serializer_class = ReactionLikeSerializer

    def get_object(self, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        Reaction.objects.get_or_create(user_reacted=self.request.user, posts=post, status=1)
        return Response({"Status 201": "Post liked succesfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post_id = self.kwargs.get('post_id')
        Reaction.objects.filter(Q(user_reacted=self.request.user) & Q(posts=post_id)).delete()
        return Response({"Status 204": "Post like deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)


class PostsLikedAPIView(generics.ListAPIView):
    """
    Class to get all the Posts that the user Liked
    """

    serializer_class = ReactionSerializer

    def get_queryset(self):
        queryset = Reaction.objects.filter(user_reacted=self.request.user)
        return queryset