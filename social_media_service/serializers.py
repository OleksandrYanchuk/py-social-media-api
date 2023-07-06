from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile, Post, Like, Follow, Comment


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "profile_picture",
            "first_name",
            "last_name",
            "bio",
            "date_of_birth",
            "location",
            "email",
            "phone",
        )

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("You already have a created profile.")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "created_at",
            "media",
            "content",
        )


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = ("username", "author")


class LikeListSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source="profile.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Like
        fields = ("profile", "post")


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source="profile.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "profile", "text", "created_at")


class FollowerListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(
        source="follower.username", read_only=True
    )

    class Meta:
        model = Follow
        fields = ("follower",)


class FollowingListSerializer(serializers.ModelSerializer):
    following = serializers.CharField(
        source="following.username", read_only=True
    )

    class Meta:
        model = Follow
        fields = ("following",)
