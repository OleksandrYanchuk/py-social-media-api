from django.test import TestCase
from django.utils import timezone

from social_media_service.models import Post, Like, Comment, Profile, Follow
from user.models import User


class BaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            username="Test_user",
            first_name="Test_first",
            last_name="Test_last",
        )
        self.post = Post.objects.create(
            author=self.profile,
            title="Test Post",
            content="This is a test post",
        )
        self.follow = Follow.objects.create(
            follower=self.profile,
            following=self.profile,
            created_at=timezone.now(),
        )
        self.like = Like.objects.create(
            profile=self.profile, post=self.post, created_at=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            profile=self.profile,
            text="This is a test comment",
            created_at=timezone.now(),
        )


class UserModelTest(BaseModelTest):
    def test_user_create(self):
        self.assertEqual(self.user.email, "test@example.com")


class ProfileModelTest(BaseModelTest):
    def test_profile_create(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.username, "Test_user")
        self.assertEqual(self.profile.first_name, "Test_first")
        self.assertEqual(self.profile.last_name, "Test_last")

    def test_profile_str(self):
        res = f"{self.profile.username}"
        self.assertEqual(str(self.profile), res)

    def test_profile_user_full_name(self):
        res = f"{self.profile.first_name} {self.profile.last_name}"
        self.assertEqual(str(self.profile.full_name), res)


class PostModelTest(BaseModelTest):
    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post")
        self.assertEqual(self.post.author, self.profile)
        self.assertIsNotNone(self.post.created_at)


class FollowModelTest(BaseModelTest):
    def test_follow_creation(self):
        self.assertEqual(self.profile, self.follow.follower)
        self.assertEqual(self.profile, self.follow.following)


class LikeModelTest(BaseModelTest):
    def test_like_create(self):
        self.assertEqual(self.profile, self.like.profile)
        self.assertEqual(self.post, self.like.post)
        self.assertIsNotNone(self.like.created_at)


class CommentModelTest(BaseModelTest):
    def test_comment_create(self):
        self.assertEqual(self.profile, self.comment.profile)
        self.assertEqual(self.post, self.comment.post)
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertIsNotNone(self.like.created_at)
