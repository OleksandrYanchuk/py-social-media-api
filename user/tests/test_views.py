from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from user.views import CreateUserView, ManageUserView


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_user(self):
        view = CreateUserView.as_view()
        request = self.factory.post(
            "/create-user/",
            {
                "email": "test@example.com",
                "password": "testpassword",
                "is_staff": False,
            },
            format="json",
        )
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": response.data["id"],
                "email": "test@example.com",
                "is_staff": False,
            },
        )

    def test_create_user_missing_email(self):
        view = CreateUserView.as_view()
        request = self.factory.post(
            "/create-user/",
            {
                "password": "testpassword",
                "is_staff": False,
            },
            format="json",
        )
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "email": ["This field is required."],
            },
        )


class ManageUserViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@example.com", password="testpassword", is_staff=False
        )

    def test_get_user(self):
        view = ManageUserView.as_view()
        request = self.factory.get("/manage-user/")
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.user.id,
                "email": "test@example.com",
                "is_staff": False,
            },
        )

    def test_unauthorized_access(self):
        view = ManageUserView.as_view()
        request = self.factory.get("/manage-user/")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        view = ManageUserView.as_view()
        request = self.factory.put(
            "/manage-user/",
            {
                "email": "updated@example.com",
                "is_staff": True,
            },
            format="json",
        )
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "email": "updated@example.com",
                "is_staff": True,
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertTrue(self.user.is_staff)




