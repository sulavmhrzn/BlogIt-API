from blog.models import Comment, Post
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class TestCommentCreate(APITestCase):
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

    def test_comment_create_returns_201(self):
        self.client.force_authenticate(self.normal_user)

        post_id = self.post1.id
        data = {"text": "test comment"}

        response = self.client.post(f"/api/post/{post_id}/comments/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_create_returns_401_for_anonymous_user(self):
        post_id = self.post1.id
        data = {"text": "test"}

        response = self.client.post(f"/api/post/{post_id}/comments/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_creates_on_right_post(self):
        self.client.force_authenticate(self.normal_user)
        post_id = self.post1.id
        data = {"text": "test"}

        response = self.client.post(f"/api/post/{post_id}/comments/", data=data)
        post1_comments_count = self.post1.comments.count()
        post2_comments_count = self.post2.comments.count()

        self.assertEqual(post1_comments_count, 1)
        self.assertEqual(post2_comments_count, 0)

    def test_comment_create_returns_400(self):
        self.client.force_authenticate(self.normal_user)
        post_id = self.post1.id
        data = {"text": ""}

        response = self.client.post(f"/api/post/{post_id}/comments/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
