from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from social_media_service.models import Profile, Post, Comment
from social_media_service.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
)
from social_media_service.views import ProfileViewSet

PROFILE_URL = reverse("social_media_service:profile-list")
POST_URL = reverse("social_media_service:post-list")


def sample_profile(**params):
    defaults = {
        "user": "",
        "first_name": "firstname",
        "last_name": "lastname",
        "username": "",
    }
    defaults.update(params)

    return Profile.objects.create(**defaults)


def sample_post(**params):
    defaults = {
        "author": "",
        "title": "",
        "content": "",
    }
    defaults.update(params)

    return Post.objects.create(**defaults)


def profile_detail_url(profile_id):
    return reverse("social_media_service:profile-detail", args=[profile_id])


def post_detail_url(post_id):
    return reverse("social_media_service:post-detail", args=[post_id])


class ProfileViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@user.com",
            password="test_password",
        )
        self.client.force_authenticate(self.user)

        self.factory = APIRequestFactory()

    def test_list_profiles(self):
        view = ProfileViewSet.as_view({"get": "list"})
        self.profile = Profile.objects.create(user=self.user, username="test_user_test")
        request = self.factory.get("/profiles/")
        force_authenticate(request, user=self.user)  # Authenticate the request
        response = view(request)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), profiles.count())
        for response_profile, serialized_profile in zip(response.data, serializer.data):
            self.assertEqual(
                response_profile["username"], serialized_profile["username"]
            )

    def test_retrieve_profile_detail(self):
        profile = sample_profile(
            user=self.user,
        )

        url = profile_detail_url(profile.id)
        res = self.client.get(url)

        serializer = ProfileSerializer(profile)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_another_profile_forbidden(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )

        profile = sample_profile(user=user)
        payload = {
            "first_name": "another",
            "last_name": "another",
            "gender": "Male",
        }
        res = self.client.put(profile_detail_url(profile.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_another_profile_forbidden(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        profile = sample_profile(user=user)
        res = self.client.delete(profile_detail_url(profile.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PostsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass1",
        )
        self.profile = sample_profile(user=self.user, username="user_name")
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        sample_post(author=self.profile)

        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_post_by_title(self):
        post1 = sample_post(author=self.profile, title="title1")
        post2 = sample_post(author=self.profile, title="title2")
        post3 = sample_post(author=self.profile, title="title3")

        res = self.client.get(POST_URL, {"title": "title1"})

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        serializer3 = PostSerializer(post3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_post_detail(self):
        post = sample_post(author=self.profile)

        url = post_detail_url(post.id)
        res = self.client.get(url)

        serializer = PostSerializer(post)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_like_post(self):
        post = sample_post(author=self.profile)

        url = reverse("social_media_service:post-like", args=[post.pk])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": f"You are liked {post.title} now."})

    def test_unlike_post(self):
        post = sample_post(author=self.profile)

        url = reverse("social_media_service:post-like", args=[post.pk])

        self.client.post(url)

        url_unlike = reverse("social_media_service:post-unlike", args=[post.pk])
        response = self.client.post(url_unlike)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": f"You have unliked {post.title}."})

    def test_comments(self):
        post = sample_post(author=self.profile)
        url = reverse("social_media_service:post-comments", args=[post.pk])
        response = self.client.get(url)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_add_comment(self):
        post = sample_post(author=self.profile)
        url = reverse("social_media_service:post-add-comment", args=[post.pk])
        data = {
            "text": "Test Comment",
        }
        response = self.client.post(url, data)
        comment = Comment.objects.get(post=post, text="Test Comment")
        serializer = CommentSerializer(comment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_comment(self):
        post = sample_post(author=self.profile)
        comment = Comment.objects.create(
            post=post, profile=self.profile, text="Old Comment"
        )
        url = reverse(
            "social_media_service:post-update-comment", args=[post.pk, comment.pk]
        )
        data = {
            "text": "Updated Comment",
        }
        response = self.client.put(url, data)
        comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.text, "Updated Comment")

    def test_delete_comment(self):
        post = sample_post(author=self.profile)
        comment = Comment.objects.create(
            post=post, profile=self.profile, text="Test Comment"
        )
        url = reverse(
            "social_media_service:post-delete-comment", args=[post.pk, comment.pk]
        )
        response = self.client.delete(url)
        exists = Comment.objects.filter(post=post, profile=self.profile).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)
