"""
This module contains tests related to user authentication and registration for the polls app.
It includes:
1. Unit tests for the RegisterForm to ensure it correctly handles user creation.
2. Functional tests to verify the registration flow and redirection.
3. Security tests to check access control for unauthenticated users.
Note: These tests are designed to be run with Django's test framework and assume
 that the relevant views and forms are implemented as per the tutorial.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from polls.forms import RegisterForm


class AuthTests(TestCase):
    """Tests for user authentication and registration in the polls app."""

    # 1. UNIT TEST: Logic of the RegisterForm
    def test_register_form_valid(self):
        """Test that the custom form correctly saves email as username."""
        form_data = {
            "email": "student@example.com",
            "password1": "secret-pass-123",
            "password2": "secret-pass-123",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "student@example.com")
        self.assertEqual(user.email, "student@example.com")

    # 2. FUNCTIONAL TEST: Flow of registration
    def test_registration_flow_redirects(self):
        """Test that submitting the registration form creates a user and redirects."""
        response = self.client.post(
            reverse("polls:register"),
            {
                "email": "newuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
            },
        )
        self.assertRedirects(response, reverse("polls:index"))
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    # 3. SECURITY TEST: Access Control (Guest vs Authenticated)
    def test_unauthenticated_user_cannot_vote(self):
        """Test that a guest user is redirected to login when trying to vote."""
        # Create a question so we don't get a 404
        from django.utils import timezone
        from polls.models import Question

        question = Question.objects.create(
            question_text="Test?", pub_date=timezone.now()
        )

        url = reverse("polls:vote", args=(question.id,))
        response = self.client.get(url)
        # Assuming we eventually use LoginRequiredMixin or @login_required
        # For now, this serves as a baseline check for protected routes.
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])
