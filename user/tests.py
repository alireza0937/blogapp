from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestRegisterViewSet(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test username", password="test password"
        )

    def test_register_with_complete_data(self):

        url = reverse("register-api-list")
        payload = {"username": "alireza", "password": "1234"}
        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Successfully registered."})

    def test_register_with_incomplete_data(self):
        url = reverse("register-api-list")
        payloads = [{"username": "test user"}, {"password": "test password"}]
        for payload in payloads:
            response = self.client.post(url, data=payload)
            error_details = list(response.data.values())[0][0]
            self.assertEqual(response.status_code, 400)
            self.assertIn("This field is required.", error_details)

    def test_register_with_duplicate_username(self):
        url = reverse("register-api-list")
        payload = {"username": "test username", "password": "test password"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("username")[0], "Username already exists.")
