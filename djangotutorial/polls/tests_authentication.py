"""
Authentication test suite for the Django Poll App.

# P.Augstein / 09.05.26 / My approach has been to let the AI generate a number of unit tests and then rewrite three of them by my own. 2 of them revealed real errors

File location:
    polls/tests_auth.py        (replace your current placeholder)

Run with:
    python manage.py test polls.tests_auth

Or a single test:
    python manage.py test polls.tests_auth.LoginFlowTests.test_login_success_redirects

============================================================
THINGS TO VERIFY before running:
============================================================

1. RegisterForm exists in polls/forms.py.
   If it has a different name, change the import below.

2. URL names — open polls/urls.py and mysite/urls.py and check
   that these names exist:
     - 'login'                  (likely from django.contrib.auth.urls)
     - 'logout'                 (likely from django.contrib.auth.urls)
     - 'register'               (your custom view — could be
                                  'register' or 'polls:register')
     - 'polls:index'
     - 'polls:results'
   If 'register' is namespaced as 'polls:register', do a search
   & replace in this file.

3. The navbar template uses literal "Login" / "Logout".
   If you use German ("Anmelden" / "Abmelden"), adjust
   assertContains() strings.

4. Default Django User model assumed.
============================================================
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from polls.forms import RegisterForm

User = get_user_model()


# ====================================================================
# 1. UNIT TESTS — Logic & Models
# ====================================================================

class RegisterFormTests(TestCase):
    """Tests the validation logic of the registration form."""

    def _valid_data(self, **overrides):
        """Helper: returns a baseline of valid form data."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        data.update(overrides)
        return data

    def test_form_valid_with_correct_data(self):
        """Sanity check — baseline data should be valid."""
        form = RegisterForm(data=self._valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_mismatch(self):
        """RegisterForm is invalid if password1 != password2."""
        form = RegisterForm(data=self._valid_data(
            password2='DifferentPass456!'
        ))
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_email_format(self):
        """RegisterForm rejects strings that aren't valid emails."""
        for bad_email in ['not-an-email', 'foo@', '@bar.com', 'plain text']:
            with self.subTest(email=bad_email):
                form = RegisterForm(data=self._valid_data(email=bad_email))
                self.assertFalse(form.is_valid())
                self.assertIn('email', form.errors)

#P. Augstein / 09.05.26 / This is the first method i am going to rewrite
class UserModelTests(TestCase):
    """This method will test whether a user is not a member of regular staff"""
    """Creates a user in the test database - Testdatabase has been be only created for testing purpose"""
    def test_default_user_is_not_member_of_staff(self):
        """New users that are created are usually not members of staff."""
        user_name = User.objects.create_user(
            username='testuser',
            password='DjangoPierre123!',
        )
        self.assertFalse(user_name.is_staff)


    


# ====================================================================
# 2. FUNCTIONAL TESTS — User Flows
# ====================================================================

class LoginFlowTests(TestCase):
    """Login success, login failure, and logout flow."""

    def setUp(self):
        self.password = 'StrongPass123!'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=self.password,
        )

    def test_login_success_redirects(self):
        """Valid credentials produce a 302 redirect."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_failure_shows_error(self):
        """Wrong credentials stay on the login page with an error."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        # Django's default error message contains "correct".
        # Adjust if you customized it.
        self.assertContains(response, 'correct')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_clears_session(self):
        """Logout removes the auth session key and login link reappears."""
        self.client.login(username='testuser', password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)

        # UI check — anonymous user should see login link in navbar
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Login')


class RegistrationGetTests(TestCase):
    """The registration page loads with an empty form."""

    def test_registration_page_renders_empty_form(self):
        response = self.client.get(reverse('polls:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_bound)


# ====================================================================
# 3. SECURITY TESTS — Access Control
# ====================================================================

class PasswordStrengthTests(TestCase):
    """Django's default password validators are enforced."""

    def test_short_password_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password('abc')

    def test_common_password_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password('password')

    def test_numeric_only_password_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password('12345678')


class AccessControlTests(TestCase):
    """Rewritten by P. Augstein / 09.05.26 / This class tests whether the results of the opll are only accessible to authenticated users"""
    """The setup method creates a sample question in the test database and a user"""
    def setUp(self):
        from polls.models import Question
        from django.utils import timezone
        self.question = Question.objects.create(
            question_text='Sample?',
            pub_date=timezone.now(),
        )
        self.user = User.objects.create_user(
            username='student',
            password='DjangoPierre123!',
        )


    def test_anonymous_redirected_from_results(self):
        """P. Augstein / Verifies that an anonymous user gets redirected to login when accessing results"""
        url = reverse('polls:results', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url.lower())


    def test_authenticated_can_view_results(self):
        """P. Augstein / Verifies if an not authenticated user can see the results"""
        self.client.login(username='student', password='DjangoPierre123!')
        url = reverse('polls:results', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SessionExpiryTests(TestCase):
    """P. Augstein / 09.05.26 --> This is to handle the session --> Logging out the user."""

    def test_logout_invalidates_session_for_subsequent_requests(self):
        User.objects.create_user(
            username='testuser',
            password='DjangoPierre123!',
        )
        self.client.login(username='testuser', password='DjangoPierre123!')
        old_session_key = self.client.session.session_key

        self.client.logout()

        # Use a fresh client simulating "another tab" with the old session id
        other_client = Client()
        if old_session_key:
            other_client.cookies['sessionid'] = old_session_key
        other_client.get(reverse('polls:index'))
        self.assertNotIn('_auth_user_id', other_client.session)


class CSRFProtectionTests(TestCase):
    """P. Augstein / POST requests without a CSRF token are rejected with 403."""

    def test_post_without_csrf_token_rejected(self):
        # Spin up a client that actually enforces CSRF (off by default in tests)
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('login'), {
            'username': 'someone',
            'password': 'whatever',
        })
        self.assertEqual(response.status_code, 403)


# ====================================================================
# 4. UI / INTEGRATION TESTS
# ====================================================================

class TemplateAuthLogicTests(TestCase):
    """{{ user.is_authenticated }} toggles the navbar links."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='DjangoPierre123!',
        )

    def test_anonymous_sees_login_link(self):
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Login')

    def test_authenticated_sees_logout_link(self):
        self.client.login(username='testuser', password='DjangoPierre123!')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Logout')


class FlashMessageTests(TestCase):
    """P. Augstein / manually rewritten 09.05.2026."""

    def test_success_message_after_registration(self):
        response = self.client.post(reverse('polls:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'DjangoPierre123!',
            'password2': 'DjangoPierre123!',
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('success' in str(m.tags).lower() for m in messages),
            f"No success message found. Got: {[str(m) for m in messages]}",
        )


# ====================================================================
# 5. ADVANCED & ROBUSTNESS TESTS
# ====================================================================

class InactiveUserLoginTests(TestCase):
    """A user with is_active=False cannot log in even with correct password."""

    def test_inactive_user_cannot_login(self):
        user = User.objects.create_user(
            username='inactive',
            password='StrongPass123!',
        )
        user.is_active = False
        user.save()

        logged_in = self.client.login(
            username='inactive',
            password='StrongPass123!',
        )
        self.assertFalse(logged_in)
        self.assertNotIn('_auth_user_id', self.client.session)


class SQLInjectionAuthTests(TestCase):
    """SQL meta-characters in auth fields neither break the query nor bypass auth."""

    INJECTION_ATTEMPTS = [
        "admin' OR '1'='1",
        "admin'; DROP TABLE auth_user; --",
        "' OR 1=1 --",
        '" OR ""="',
        "admin'/*",
    ]

    def setUp(self):
        User.objects.create_user(
            username='admin',
            password='RealStrongPass123!',
        )

    def test_injection_attempts_do_not_authenticate(self):
        for attempt in self.INJECTION_ATTEMPTS:
            with self.subTest(attempt=attempt):
                logged_in = self.client.login(
                    username=attempt,
                    password='anything',
                )
                self.assertFalse(logged_in)

    def test_injection_does_not_raise_exception(self):
        for attempt in self.INJECTION_ATTEMPTS:
            with self.subTest(attempt=attempt):
                try:
                    self.client.login(username=attempt, password='x')
                except Exception as e:
                    self.fail(
                        f"Login raised an exception for input {attempt!r}: {e}"
                    )

    def test_user_table_still_intact_after_injection_attempts(self):
        """Sanity: the auth_user table wasn't dropped."""
        for attempt in self.INJECTION_ATTEMPTS:
            self.client.login(username=attempt, password='x')
        self.assertEqual(User.objects.filter(username='admin').count(), 1)


class EmailCaseSensitivityTests(TestCase):
    """
    Documents and tests the team's chosen behavior for email case.

    Django's default User.email field is CASE-SENSITIVE in lookups.
    Best practice for auth is usually CASE-INSENSITIVE — this requires
    normalizing emails to lowercase on save.

    Pick ONE of the two tests below and remove (or invert) the other,
    matching the behavior you actually want.
    """

    def test_emails_are_case_insensitive(self):
        """
        EXPECTED if you normalize emails to lowercase on save.
        """
        User.objects.create_user(
            username='user1',
            email='student@example.com',
            password='StrongPass123!',
        )
        same_email_different_case = User.objects.filter(
            email__iexact='Student@Example.com'
        )
        self.assertEqual(same_email_different_case.count(), 1)

    def test_emails_are_case_sensitive_django_default(self):
        """
        EXPECTED with Django's out-of-the-box behavior (no normalization).

        If your team has decided on case-insensitive emails, DELETE this test
        and only keep test_emails_are_case_insensitive above.
        """
        User.objects.create_user(
            username='user1',
            email='student@example.com',
            password='StrongPass123!',
        )
        self.assertTrue(
            User.objects.filter(email='student@example.com').exists()
        )
        self.assertFalse(
            User.objects.filter(email='Student@Example.com').exists()
        )
