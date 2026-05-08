"""
polls/tests_auth.py
Team Alfa — Authentication Feature Tests
Covers all cases in AUTH_TEST_PLAN.md

Run with:
    python manage.py test polls.tests_auth
"""

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from polls.forms import RegisterForm
from polls.models import Question


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_user(username="testuser", email="test@example.com",
              password="Orbit!River#4829", active=True):
    user = User.objects.create_user(
        username=username, email=email, password=password
    )
    user.is_active = active
    user.save()
    return user


def make_question(text="Test question?"):
    return Question.objects.create(
        question_text=text, pub_date=timezone.now()
    )


# ---------------------------------------------------------------------------
# 1. Unit Tests — Form & Model
# ---------------------------------------------------------------------------

class RegisterFormTests(TestCase):

    def test_register_form_valid(self):
        """Abel's original test — valid email+password saves email as username."""
        form = RegisterForm(data={
            "email": "student@example.com",
            "password1": "secret-pass-123",
            "password2": "secret-pass-123",
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "student@example.com")
        self.assertEqual(user.email, "student@example.com")

    def test_form_password_mismatch(self):
        """Form is invalid when password1 and password2 don't match."""
        form = RegisterForm(data={
            "email": "alice@example.com",
            "password1": "Orbit!River#4829",
            "password2": "DifferentPass#999",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_email(self):
        """Form rejects strings that are not valid email addresses."""
        form = RegisterForm(data={
            "email": "notanemail",
            "password1": "Orbit!River#4829",
            "password2": "Orbit!River#4829",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_model_user_creation_default_permissions(self):
        """Newly created users are not staff or superuser by default."""
        user = make_user(username="bob", email="bob@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


# ---------------------------------------------------------------------------
# 2. Functional Tests — User Flows
# ---------------------------------------------------------------------------

class LoginTests(TestCase):

    def setUp(self):
        self.email = "dana@example.com"
        self.password = "Orbit!River#4829"
        make_user(username=self.email, email=self.email, password=self.password)

    def test_login_success_redirects(self):
        """Valid credentials redirect to the polls index."""
        response = self.client.post(reverse("login"), {
            "username": self.email,
            "password": self.password,
        })
        self.assertRedirects(response, reverse("polls:index"))

    def test_login_failure_shows_error(self):
        """Wrong password keeps user on login page and does not authenticate."""
        response = self.client.post(reverse("login"), {
            "username": self.email,
            "password": "WrongPassword#99",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutTests(TestCase):

    def setUp(self):
        self.email = "eve@example.com"
        self.password = "Orbit!River#4829"
        make_user(username=self.email, email=self.email, password=self.password)

    def test_logout_clears_session(self):
        """After logout the user is no longer authenticated."""
        self.client.login(username=self.email, password=self.password)
        self.client.logout()
        response = self.client.get(reverse("polls:index"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_ui_shows_login_link(self):
        """After logout the navbar shows Login, not Logout."""
        self.client.login(username=self.email, password=self.password)
        self.client.logout()
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Login")


class RegistrationFlowTests(TestCase):

    def test_registration_flow_redirects(self):
        """Abel's original test — valid POST redirects to index."""
        response = self.client.post(reverse("polls:register"), {
            "email": "newuser@example.com",
            "password1": "Orbit!River#4829",
            "password2": "Orbit!River#4829",
        })
        self.assertRedirects(response, reverse("polls:index"))
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_registration_get_loads_empty_form(self):
        """GET /register/ returns 200 with an empty form with no errors."""
        response = self.client.get(reverse("polls:register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(len(response.context["form"].errors), 0)


# ---------------------------------------------------------------------------
# 3. Security Tests
# ---------------------------------------------------------------------------

class PasswordStrengthTests(TestCase):

    def test_weak_password_rejected(self):
        """Django's validators reject a password that is too short/simple."""
        form = RegisterForm(data={
            "email": "henry@example.com",
            "password1": "123",
            "password2": "123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_common_password_rejected(self):
        """Django's CommonPasswordValidator rejects 'password' as too common."""
        form = RegisterForm(data={
            "email": "ivan@example.com",
            "password1": "password",
            "password2": "password",
        })
        self.assertFalse(form.is_valid())


class AccessControlTests(TestCase):

    def setUp(self):
        self.question = make_question()
        self.email = "judy@example.com"
        self.password = "Orbit!River#4829"
        make_user(username=self.email, email=self.email, password=self.password)

    def test_unauthenticated_user_cannot_vote(self):
        """Abel's original test — guests are redirected to login on vote."""
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_results_page_visible_to_anonymous_user(self):
        """
        ResultsView is currently NOT protected by @login_required.
        This test documents that behavior.
        """
        url = reverse("polls:results", args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_session_expiry_after_logout(self):
        """After logout, the same client is redirected away from protected pages."""
        self.client.login(username=self.email, password=self.password)
        self.client.logout()
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_csrf_protection_on_login(self):
        """POST to login without a CSRF token returns 403."""
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse("login"), {
            "username": self.email,
            "password": self.password,
        })
        self.assertEqual(response.status_code, 403)


# ---------------------------------------------------------------------------
# 4. UI / Integration Tests
# ---------------------------------------------------------------------------

class NavbarTemplateLogicTests(TestCase):

    def setUp(self):
        self.email = "karen@example.com"
        self.password = "Orbit!River#4829"
        make_user(username=self.email, email=self.email, password=self.password)

    def test_navbar_shows_logout_when_authenticated(self):
        """Logged-in users see Logout in the navbar."""
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Logout")

    def test_navbar_shows_login_when_anonymous(self):
        """Anonymous users see Login and Register in the navbar."""
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Login")
        self.assertContains(response, "Register")


# ---------------------------------------------------------------------------
# 5. Advanced & Robustness Tests
# ---------------------------------------------------------------------------

class RobustnessTests(TestCase):

    def test_inactive_user_cannot_log_in(self):
        """A user with is_active=False cannot authenticate."""
        email = "leo@example.com"
        password = "Orbit!River#4829"
        make_user(username=email, email=email, password=password, active=False)
        logged_in = self.client.login(username=email, password=password)
        self.assertFalse(logged_in)

    def test_sql_injection_in_login_does_not_crash(self):
        """SQL characters in the username field do not cause a 500 or auth bypass."""
        response = self.client.post(reverse("login"), {
            "username": "' OR '1'='1",
            "password": "Orbit!River#4829",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_sql_injection_in_registration_does_not_crash(self):
        """SQL characters in the email field during registration are handled safely."""
        response = self.client.post(reverse("polls:register"), {
            "email": "'; DROP TABLE auth_user; --",
            "password1": "Orbit!River#4829",
            "password2": "Orbit!River#4829",
        })
        self.assertNotEqual(response.status_code, 500)

    def test_email_case_sensitivity(self):
        """
        Django usernames are case-sensitive by default.
        Student@Example.com and student@example.com are treated as two
        different users. This documents that as the intended behavior.
        """
        self.client.post(reverse("polls:register"), {
            "email": "Student@Example.com",
            "password1": "Orbit!River#4829",
            "password2": "Orbit!River#4829",
        })
        self.client.post(reverse("polls:register"), {
            "email": "student@example.com",
            "password1": "Orbit!River#4829",
            "password2": "Orbit!River#4829",
        })
        self.assertTrue(User.objects.filter(username="Student@Example.com").exists())
        self.assertTrue(User.objects.filter(username="student@example.com").exists())