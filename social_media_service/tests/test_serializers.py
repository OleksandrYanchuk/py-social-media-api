from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from social_media_service.models import Post, Comment, Profile, Like, Follow
from social_media_service.serializers import (
    PostSerializer,
    ProfileSerializer,
    CommentSerializer,
    PostListSerializer,
    LikeListSerializer,
    FollowerListSerializer,
    FollowingListSerializer,
)
from user.models import User
from user.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@example.com", password="userpass"
        )
        self.factory = APIRequestFactory()
        request = self.factory.get("/dummy_url/")
        self.context = {"request": Request(request)}

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user, context=self.context)
        expected_data = {
            "id": self.user.id,
            "email": self.user.email,
            "is_staff": False,
        }
        self.assertEqual(serializer.data, expected_data)


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.profile_data = {
            "username": "test_user",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_profile_serializer_create(self):
        serializer = ProfileSerializer(data=self.profile_data)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save(user=self.user)
        self.assertEqual(profile.username, self.profile_data["username"])

    def test_profile_serializer_update(self):
        profile = Profile.objects.create(
            user=self.user, username="old_username", first_name="Old", last_name="Name"
        )
        serializer = ProfileSerializer(instance=profile, data=self.profile_data)
        self.assertTrue(serializer.is_valid())
        updated_profile = serializer.save()
        self.assertEqual(updated_profile.username, self.profile_data["username"])


class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.profile = Profile.objects.create(
            user=self.user, username="old_username", first_name="Old", last_name="Name"
        )

        self.post_data = {
            "title": "Test Post",
            "content": "This is a test post",
            "author": self.profile.pk,
        }

    def test_post_serializer_create(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(
            serializer.is_valid(), serializer.errors
        )  # Print serializer errors
        post = serializer.save()
        self.assertEqual(post.title, self.post_data["title"])

    def test_post_serializer_update(self):
        post = Post.objects.create(
            title="Old Title", content="Old Content", author=self.profile
        )
        serializer = PostSerializer(instance=post, data=self.post_data)
        self.assertTrue(serializer.is_valid())
        updated_post = serializer.save()
        self.assertEqual(updated_post.title, self.post_data["title"])


class PostListSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="userpass"
        )
        self.profile = Profile.objects.create(
            user=self.user, first_name="Old", last_name="Name", username="Test_user"
        )
        self.factory = APIRequestFactory()
        request = self.factory.get("/dummy_url/")
        self.context = {"request": Request(request)}

    def test_post_list_serializer(self):
        post = Post.objects.create(
            author=self.profile, title="Test Post", content="This is a test post"
        )
        serializer = PostListSerializer(instance=post, context=self.context)
        expected_data = {"title": "Test Post", "author": self.profile.username}
        self.assertEqual(serializer.data, expected_data)


class LikeListSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="userpass"
        )
        self.profile = Profile.objects.create(user=self.user, username="test_user")
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", author=self.profile
        )

    def test_like_list_serializer(self):
        like = Like.objects.create(profile=self.profile, post=self.post)
        serializer = LikeListSerializer(instance=like)
        expected_data = {
            "profile": self.profile.username,
            "post": self.post.title,
        }
        self.assertEqual(serializer.data, expected_data)


class FollowerListSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="userpass"
        )
        self.profile = Profile.objects.create(user=self.user, username="test_user")

    def test_follower_list_serializer(self):
        follow = Follow.objects.create(follower=self.profile, following=self.profile)
        serializer = FollowerListSerializer(instance=follow)
        expected_data = {
            "follower": self.profile.username,
        }
        self.assertEqual(serializer.data, expected_data)


class FollowingListSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="userpass"
        )
        self.profile = Profile.objects.create(user=self.user, username="test_user")

    def test_following_list_serializer(self):
        follow = Follow.objects.create(follower=self.profile, following=self.profile)
        serializer = FollowingListSerializer(instance=follow)
        expected_data = {
            "following": self.profile.username,
        }
        self.assertEqual(serializer.data, expected_data)


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="userpass"
        )
        self.profile = Profile.objects.create(user=self.user, username="test_user")
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", author=self.profile
        )

    def test_comment_serializer(self):
        comment = Comment.objects.create(
            post=self.post,
            profile=self.profile,
            text="This is a test comment",
            created_at=timezone.now(),
        )
        serializer = CommentSerializer(instance=comment)
        expected_data = {
            "id": comment.id,
            "post": self.post.title,
            "profile": self.profile.username,
            "text": "This is a test comment",
            "created_at": comment.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),  # Include the actual created_at value
        }
        self.assertEqual(serializer.data, expected_data)
