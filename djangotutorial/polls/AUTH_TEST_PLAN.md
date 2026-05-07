# How to run tests

python manage.py test polls.tests_auth

# Proposed Test Cases

To provide comprehensive coverage for the authentication feature, students should implement the following tests:

## 1. Unit Tests (Logic & Models)
- [ ] **Form: Password Mismatch** - Verify `RegisterForm` is invalid if `password1` and `password2` don't match.
- [ ] **Form: Invalid Email** - Verify `RegisterForm` rejects strings that aren't valid email addresses.
- [ ] **Model: User Creation** - Verify default user permissions (is_staff should be False by default).

## 2. Functional Tests (User Flows)
- [ ] **Login Success** - Verify standard Django login redirect works.
- [ ] **Login Failure** - Verify error messages appear on the login page with wrong credentials.
- [ ] **Logout Flow** - Verify `self.client.logout()` clears the session and the UI updates (e.g., "Login" button reappears).
- [ ] **Registration GET** - Verify the registration page loads with an empty form.

## 3. Security Tests (Access Control)
- [ ] **Password Strength** - Test that the system enforces Django's default password validators.
- [ ] **Login Required: Results** - Ensure poll results are only visible to registered students (if applicable).
- [ ] **Session Expiry** - Verify that logging out on one device/tab expires the session.
- [ ] **CSRF Protection** - (Intermediate) Verify that POST requests without a CSRF token are rejected (403).

## 4. UI/Integration Tests
- [ ] **Template Logic** - Test that `{{ user.is_authenticated }}` correctly toggles "Register/Login" vs "Logout" links in the navbar.
- [ ] **Flash Messages** - Verify that a success message appears after a user successfully registers.

## 5. Advanced & Robustness Tests
- [ ] **Inactive User** - Verify that a user with `is_active=False` cannot log in, even with correct credentials.
- [ ] **SQL Injection in Auth** - Verify that putting SQL characters in the email/username field does not break the query or allow bypass.
- [ ] **Email Case Sensitivity** - Since we use email as a username, verify if `Student@Example.com` and `student@example.com` are treated as the same user or different ones (and decide on the intended behavior).
