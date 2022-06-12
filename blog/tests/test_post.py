from blog.models import Post
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

BASE_URL = "/api/post/"


class TestPostCreate(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create(
            username="test", email="test@mail.com", password="testuser"
        )
        self.data = {
            "title": "test",
            "description": "test",
            "tags": ["tag"],
        }

    def test_post_create_returns_201(self):
        self.client.force_authenticate(self.normal_user)

        response = self.client.post(
            BASE_URL,
            data=self.data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_create_return_400(self):
        self.client.force_authenticate(self.normal_user)
        data = {"title": ""}

        response = self.client.post(f"{BASE_URL}", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_returns_401_for_anonymous_user(self):
        response = self.client.post(f"{BASE_URL}", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create_sends_email(self):
        self.client.force_authenticate(self.normal_user)

        response = self.client.post(
            f"{BASE_URL}",
            data=self.data,
            format="json",
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(mail.outbox[0].subject)


class TestPostList(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create(
            username="test", email="test@mail.com", password="testuser"
        )
        self.staff_user = User.objects.create(
            username="staff", email="staff@mail.com", password="testuser", is_staff=True
        )
        self.post1 = Post.objects.create(
            title="test", description="test", tags=["tag1"], author=self.normal_user
        )
        self.post2 = Post.objects.create(
            title="test",
            description="test",
            tags=["tag1"],
            author=self.normal_user,
            is_active=False,
        )

    def test_post_list_returns_401_for_anonymous_users(self):
        response = self.client.get(f"{BASE_URL}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_list_count_returns_greater_than_0(self):
        self.client.force_authenticate(self.normal_user)

        response = self.client.get(f"{BASE_URL}")

        self.assertGreater(response.data["count"], 0)

    def test_post_list_returns_is_active_only_for_non_staff_users(self):
        self.client.force_authenticate(self.normal_user)

        response = self.client.get(f"{BASE_URL}")

        self.assertEqual(response.data["count"], 1)

    def test_post_list_returns_all_post_for_staff_users(self):
        self.client.force_authenticate(self.staff_user)

        response = self.client.get(f"{BASE_URL}")

        self.assertEqual(response.data["count"], 2)


class TestPostRetrieve(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create(
            username="test", email="test@mail.com", password="testuser"
        )

        self.post1 = Post.objects.create(
            title="test", description="test", tags=["tag1"], author=self.normal_user
        )

    def test_post_retrieve_returns_200(self):
        self.client.force_authenticate(self.normal_user)
        post_id = self.post1.id

        response = self.client.get(f"{BASE_URL}{post_id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_retrieve_returns_404(self):
        self.client.force_authenticate(self.normal_user)

        response = self.client.get(f"{BASE_URL}123/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_retrieve_returns_401_for_anonymous_user(self):
        response = self.client.get(f"{BASE_URL}{self.post1.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPostUpdate(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create(
            username="test", email="test@mail.com", password="testuser"
        )
        self.staff_user = User.objects.create(
            username="staff", email="staff@mail.com", password="testuser", is_staff=True
        )
        self.post1 = Post.objects.create(
            title="test", description="test", author=self.normal_user
        )
        self.post2 = Post.objects.create(
            title="test", description="test", author=self.staff_user
        )

    def test_post_update_returns_updated_data(self):
        self.client.force_authenticate(self.normal_user)
        data = {"title": "updated", "description": self.post1.description, "tags": ""}
        post_id = self.post1.id

        response = self.client.put(f"{BASE_URL}{post_id}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "updated")

    def test_post_update_returns_401_for_anonymous_user(self):
        response = self.client.put(f"{BASE_URL}{self.post1.id}/", data={"title": ""})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_user_cannot_update_others_post(self):
        self.client.force_authenticate(self.normal_user)
        data = {"title": "updated", "description": self.post2.description, "tags": ""}
        post_id = self.post2.id

        response = self.client.put(f"{BASE_URL}{post_id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_update_others_post(self):
        self.client.force_authenticate(self.staff_user)
        data = {"title": "updated", "description": self.post1.description, "tags": ""}
        post_id = self.post1.id

        response = self.client.put(f"{BASE_URL}{post_id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostDelete(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create(
            username="test", email="test@mail.com", password="testuser"
        )
        self.staff_user = User.objects.create(
            username="staff", email="staff@mail.com", password="testuser", is_staff=True
        )
        self.post1 = Post.objects.create(
            title="test", description="test", tags=["tag1"], author=self.normal_user
        )
        self.post2 = Post.objects.create(
            title="test", description="test", tags=["tag1"], author=self.staff_user
        )

    def test_post_delete_returns_204(self):
        self.client.force_authenticate(self.normal_user)
        post_id = self.post1.id

        response = self.client.delete(f"{BASE_URL}{post_id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_delete_only_their_post(self):
        self.client.force_authenticate(self.normal_user)
        post_id = self.post2.id

        response = self.client.delete(f"{BASE_URL}{post_id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_delete_all_post(self):
        self.client.force_authenticate(self.staff_user)
        post_id = self.post1.id

        response = self.client.delete(f"{BASE_URL}{post_id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
