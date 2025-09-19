from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest import mock


class APISmokeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "strongpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Ensure profile created via signal
        self.user.refresh_from_db()

    def auth(self):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {"username": self.username, "password": self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_register_and_login(self):
        # Register
        resp = self.client.post(reverse('register'), {"username": "newbie", "password": "newpassword"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Login
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "newbie", "password": "newpassword"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

    def test_me_requires_auth(self):
        resp = self.client.get(reverse('me'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.auth()
        resp = self.client.get(reverse('me'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], self.username)

    def test_add_credits_admin_only(self):
        # Non-admin should be forbidden
        self.auth()
        resp = self.client.post(reverse('add_credits'), {"user_id": self.user.id, "amount": 5}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # Admin can add
        admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "admin", "password": "adminpass"}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.post(reverse('add_credits'), {"user_id": self.user.id, "amount": 5}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['credits'], 5)

    def test_chat_thread_and_message(self):
        self.auth()
        # Create thread
        resp = self.client.post(reverse('chat_thread_list_create'), {"title": "My Chat"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        thread_id = resp.data['id']
        # Post message
        resp = self.client.post(reverse('chat_message_create', kwargs={"thread_id": thread_id}), {"role": "user", "content": "Hello"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['messages']), 1)

    @mock.patch('api.views.select_service')
    def test_image_job_generation_and_credits(self, mock_select):
        # Add credits to user via admin
        admin = User.objects.create_superuser(username='admin2', password='adminpass', email='a@g.com')
        # Login admin
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "admin2", "password": "adminpass"}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        self.client.post(reverse('add_credits'), {"user_id": self.user.id, "amount": 3}, format='json')
        # Login as user
        resp = self.client.post(reverse('token_obtain_pair'), {"username": self.username, "password": self.password}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        # Mock provider to return 2 images
        service_instance = mock.Mock()
        service_instance.generate.return_value = ["b64img1", "b64img2"]
        mock_select.return_value = service_instance
        # Create job
        resp = self.client.post(reverse('image_job_list_create'), {"provider": "openai", "model": "gpt-image-1", "prompt": "a cat"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['status'], 'completed')
        self.assertEqual(len(resp.data['output_images']), 2)
        # Check credits deducted and usage updated
        me = self.client.get(reverse('me')).data
        self.assertEqual(me['profile']['credits'], 2)
        self.assertEqual(me['profile']['total_images_generated'], 2)
