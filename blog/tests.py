from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Comment, Posts
from django.contrib.auth.models import User


class TestPostViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test user", password="1234")
        cls.post1 = Posts.objects.create(
            title="Title1 for testing",
            content="Content1 for testing",
        )
        cls.post2 = Posts.objects.create(
            title="Title2 for testing",
            content="Content2 for testing",
        )

    def setUp(self):
        self.payload = {"username": "test 1", "password": "test 1"}
        self.register_new_user()
        self.retrive_user_jwt()

    def register_new_user(self):
        self.client.post(
            reverse("register-api-list"),
            data=self.payload,
        )

    def retrive_user_jwt(self):
        response = self.client.post(reverse("token_obtain_pair"), data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token = response.json().get("access")
        self.headers = {"Authorization": f"Bearer {self.jwt_token}"}

    def test_list_posts(self):
        response = self.client.get(reverse("posts-api-list"), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_user_with_wrong_jwt(self):
        headers = {"Authorization": "exampletoken"}
        response = self.client.get(reverse("posts-api-list"), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.",
            response.json().get("detail"),
        )

    def test_create_post_with_insufficient_parameters(self):
        payload1 = {"title": "test title"}
        payload2 = {"content": "test content"}

        for payload in [payload1, payload2]:
            response = self.client.post(
                reverse("posts-api-list"), headers=self.headers, data=payload
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_details = list(response.data.values())[0][0]
            self.assertIn("This field is required.", error_details)

    def test_create_post_with_wrong_jwt(self):
        headers = {"Authorization": "exampletoken"}
        payload = {"title": "test title", "content": "test content"}
        response = self.client.post(
            reverse("posts-api-list"), headers=headers, data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_create_post_with_sufficient_parameters(self):
        payload = {"title": "test title", "content": "test content"}
        response = self.client.post(
            reverse("posts-api-list"), headers=self.headers, data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_posts_with_wrong_id(self):
        url = reverse("posts-api-detail", kwargs={"pk": 122})
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "No Posts matches the given query.")

    def test_retrieve_posts_with_correct_id(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_posts_with_wrong_jwt(self):
        headers = {"Authorization": "exampletoken"}
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_update_posts_with_proper_data(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        payload = {"title": "update title", "content": "update content"}
        response = self.client.put(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_posts_with_incomplete_data(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})

        for payload in [{"title": "update title"}, {"content": "update content"}]:
            response = self.client.put(url, headers=self.headers, data=payload)
            error_details = list(response.data.values())[0][0]
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("This field is required.", error_details)

    def test_update_posts_with_wrong_jwt(self):
        headers = {"Authorization": "exampletoken"}
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        payload = {"title": "update title", "content": "update content"}
        response = self.client.put(url, headers=headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )


class TestCommentViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test user", password="1234")
        cls.post1 = Posts.objects.create(
            title="Title1 for testing",
            content="Content1 for testing",
        )
        cls.post2 = Posts.objects.create(
            title="Title2 for testing",
            content="Content2 for testing",
        )

        cls.comment1 = Comment.objects.create(
            text="test text", email="test@test.com", post=cls.post1
        )

    def setUp(self):
        self.payload = {"username": "test 1", "password": "test 1"}
        self.register_new_user()
        self.retrive_user_jwt()

    def register_new_user(self):
        self.client.post(
            reverse("register-api-list"),
            data=self.payload,
        )

    def retrive_user_jwt(self):
        response = self.client.post(reverse("token_obtain_pair"), data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.jwt_token = response.json().get("access")
        self.headers = {"Authorization": f"Bearer {self.jwt_token}"}

    def test_list_comment(self):
        url = reverse("comments-api-list")
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_list_comments_with_wrong_jwt(self):
        headers = {"Authorization": "wrongjwttoken"}
        url = reverse("comments-api-list")
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_create_comment_with_wrong_email(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test email for comment",
            "post": self.post1.pk,
        }
        response = self.client.post(url, headers=self.headers, data=payload)
        self.assertEqual(
            response.json().get("email")[0], "Enter a valid email address."
        )
        self.assertEqual(response.status_code, 400)

    def test_reply_comment_with_correct_post_id(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post1.pk,
            "answer": self.comment1.pk,
        }
        response = self.client.post(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 201)

    def test_reply_comment_with_wrong_post_id(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post2.pk,
            "answer": self.comment1.pk,
        }
        response = self.client.post(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("answer")[0],
            "Parent comment does not belong to the same post.",
        )

    def test_reply_comment_with_wrong_user_jwt(self):
        headers = {"Authorization": "wrongjwttoken"}
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post2.pk,
            "answer": self.comment1.pk,
        }
        response = self.client.post(url, headers=headers, data=payload)
        self.assertEqual(
            "Authentication credentials were not provided.",
            response.json().get("detail"),
        )

    def test_create_comment_with_wrong_post_id(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": 122,
        }
        response = self.client.post(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get("post")[0],
            """Invalid pk "122" - object does not exist.""",
        )

    def test_create_comment_with_incomplete_data(self):
        url = reverse("comments-api-list")
        payloads = [{"text": "test text for comment"}, {"email": "test@test.com"}]
        for payload in payloads:
            response = self.client.post(url, headers=self.headers, data=payload)
            error_details = list(response.data.values())[0][0]
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("This field is required.", error_details)

    def test_create_comment_with_complete_data(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post1.pk,
        }
        response = self.client.post(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_wrong_jwt(self):
        headers = {"Authorization": "wrongjwttoken"}
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post1.pk,
        }
        url = reverse("comments-api-list")
        response = self.client.post(url, headers=headers, data=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json().get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_comment_view_with_irrelevant_request_method(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post1.pk,
        }
        response = self.client.put(url, headers=self.headers, data=payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json()["detail"], """Method "PUT" not allowed.""")
