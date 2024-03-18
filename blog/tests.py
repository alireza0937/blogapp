from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Posts


class TestPostViewSet(APITestCase):
    def setUp(self):
        self.post1 = Posts.objects.create(
            title="Title1 for testing",
            content="Content1 for testing",
        )
        self.post2 = Posts.objects.create(
            title="Title2 for testing",
            content="Content2 for testing",
        )
        self.url_list = reverse("posts-api-list")

    def test_list_posts(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_post_with_insufficient_parameters(self):
        payload1 = {"title": "test title"}
        payload2 = {"content": "test content"}

        for payload in [payload1, payload2]:
            response = self.client.post(self.url_list, data=payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_details = list(response.data.values())[0][0]
            self.assertIn("This field is required.", error_details)

    def test_create_post_with_sufficient_parameters(self):
        payload = {"title": "test title", "content": "test content"}
        response = self.client.post(self.url_list, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_posts_with_wrong_id(self):
        url = reverse("posts-api-detail", kwargs={"pk": 122})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "No Posts matches the given query.")

    def test_retrieve_posts_with_correct_id(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_posts_with_proper_data(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})
        payload = {"title": "update title", "content": "update content"}
        response = self.client.put(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_posts_with_incomplete_data(self):
        url = reverse("posts-api-detail", kwargs={"pk": self.post1.pk})

        for payload in [{"title": "update title"}, {"content": "update content"}]:
            response = self.client.put(url, data=payload)
            error_details = list(response.data.values())[0][0]
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("This field is required.", error_details)


class TestCommentViewSet(APITestCase):

    def setUp(self):
        self.post1 = Posts.objects.create(
            title="Title1 for testing Comments",
            content="Content1 for testing Comments",
        )

    def test_list_comment(self):
        url = reverse("comments-api-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_create_comment_with_wrong_email(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test email for comment",
            "post": self.post1.pk,
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(
            response.json().get("email")[0], "Enter a valid email address."
        )
        self.assertEqual(response.status_code, 400)

    def test_create_comment_with_wrong_post_id(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": 122,
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get("post")[0],
            """Invalid pk "122" - object does not exist.""",
        )

    def test_create_comment_with_incomplete_data(self):
        url = reverse("comments-api-list")
        payloads = [{"text": "test text for comment"}, {"email": "test@test.com"}]
        for payload in payloads:
            response = self.client.post(url, data=payload)
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
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), payload)

    def test_comment_view_with_irrelevant_request_method(self):
        url = reverse("comments-api-list")
        payload = {
            "text": "test text for comment",
            "email": "test@test.com",
            "post": self.post1.pk,
        }
        response = self.client.put(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json()["detail"], """Method "PUT" not allowed.""")
