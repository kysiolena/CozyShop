from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authapp.models import Profile
from authapp.tasks import send_email_task

User = get_user_model()


class AuthModelTest(TestCase):
    """
    Tests for Auth models and Signals (models.py).
    """

    def test_create_user_creates_profile_signal(self):
        """Test that creating a User automatically creates a linked Profile."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

        # Check profile existence
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.user, user)

    def test_custom_user_string_representation(self):
        """Test that the CustomUser string representation is the email."""
        user = User.objects.create_user(
            username="strtest", email="str@example.com", password="password123"
        )
        self.assertEqual(str(user), "str@example.com")

    def test_profile_img_property(self):
        """Test the profile image property returns correct fallback."""
        user = User.objects.create_user(
            username="imgtest", email="img@example.com", password="password123"
        )
        # No image uploaded
        self.assertIn("image-not-found.png", user.profile.img)


class AuthViewTest(TestCase):
    """
    Tests for the Auth Views (endpoints).
    """

    def setUp(self):
        self.client = Client()

        # Create an active user for login tests
        self.user = User.objects.create_user(
            username="activeuser", email="active@test.com", password="password123"
        )

        # Create an inactive user for activation tests
        self.inactive_user = User.objects.create_user(
            username="inactiveuser", email="inactive@test.com", password="password123"
        )
        self.inactive_user.is_active = False
        self.inactive_user.save()

    @patch("authapp.views.send_email_task.delay")
    def test_sign_up_view_success(self, mock_email_task):
        """Test registration creates inactive user and calls email task."""
        url = reverse("sign_up_page")

        # Use a stronger password to pass Django's validators (CommonPasswordValidator)
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = self.client.post(url, data)

        # Check redirection
        self.assertRedirects(response, reverse("shop_page"))

        # Check user created but inactive
        new_user = User.objects.get(email="new@test.com")
        self.assertFalse(new_user.is_active)

        # Check email task was triggered
        self.assertTrue(mock_email_task.called)

    def test_activate_account_view_success(self):
        """Test that a valid token activates the user."""
        uid = urlsafe_base64_encode(force_bytes(self.inactive_user.pk))
        token = default_token_generator.make_token(self.inactive_user)

        url = reverse("activate_page", kwargs={"uidb64": uid, "token": token})

        response = self.client.get(url)

        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)
        self.assertRedirects(response, reverse("sign_in_page"))

    def test_activate_account_view_invalid(self):
        """Test that an invalid token does not activate user."""
        uid = urlsafe_base64_encode(force_bytes(self.inactive_user.pk))
        url = reverse("activate_page", kwargs={"uidb64": uid, "token": "invalid-token"})

        response = self.client.get(url)

        self.inactive_user.refresh_from_db()
        self.assertFalse(self.inactive_user.is_active)
        self.assertRedirects(response, reverse("shop_page"))

    def test_sign_in_view(self):
        """Test valid login."""
        url = reverse("sign_in_page")
        data = {"username": "active@test.com", "password": "password123"}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("shop_page"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_sign_out_view(self):
        """Test logout."""
        self.client.force_login(self.user)
        url = reverse("sign_out_page")

        # Django 5.x LogoutView requires POST to prevent CSRF
        response = self.client.post(url)

        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(response, reverse("sign_in_page"))

    def test_profile_update_view(self):
        """Test updating profile information."""
        self.client.force_login(self.user)
        url = reverse("profile_page")

        data = {
            "username": "updatedname",
            "email": "active@test.com",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(url, data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updatedname")
        self.assertEqual(self.user.first_name, "John")

    @patch("authapp.views.send_email_task.delay")
    def test_profile_delete_request(self, mock_email_task):
        """Test requesting profile deletion sends an email."""
        self.client.force_login(self.user)
        url = reverse("profile_delete_page")

        # Trigger delete request (POST)
        response = self.client.post(url)

        self.assertTrue(mock_email_task.called)
        # User should still exist until confirmed
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_profile_delete_confirm(self):
        """Test confirming profile deletion removes the user."""
        self.client.force_login(self.user)

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse(
            "profile_delete_confirm_page", kwargs={"uidb64": uid, "token": token}
        )

        response = self.client.get(url)

        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertRedirects(response, reverse("shop_page"))

    def test_reset_password_view(self):
        """
        Test password reset request.
        """
        url = reverse("reset_password_page")
        data = {"email": "active@test.com"}

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, 302
        )  # Redirects to success URL (shop_page)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("active@test.com", mail.outbox[0].to)


class AuthTaskTest(TestCase):
    """
    Tests for Celery tasks (tasks.py).
    """

    def test_send_email_task(self):
        """Test the shared celery task wrapper calls Django send_mail."""

        # Clear outbox
        mail.outbox = []

        subject = "Task Test"
        body = "Body content"
        to = ["task@test.com"]

        # Call the task function directly (synchronously for testing)
        send_email_task(
            to_emails=to,
            from_email="admin@cozyshop.com",
            subject=subject,
            html_body="<p>Body</p>",
            body=body,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].to, to)
