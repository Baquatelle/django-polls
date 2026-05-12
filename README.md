# uds-cc1-wup — Django Polls Extension

**Team Alfa - Coding Camp 1 - Warmup Project**

An extension of the official Django tutorial polls app, adding user authentication built on top of Django's built-in `contrib.auth` system.

---

## What the App Does

- Users can register an account, log in, and log out
- Unauthenticated users are redirected to login before they can vote
- The polls app (questions and choices) runs as per the Django tutorial baseline

> **Note:** The voting choices feature is not working. The Personal Voting History page was planned but not implemented within the project timeline.

---

## Team

| # | Role | Responsibility |
|---|------|----------------|
| 1 | Auth Lead | Login, logout, and registration pages |
| 2 | Model Lead | UserVote model, migration, admin registration |
| 3 | Voting Lead | Securing vote() — login required, no double-voting |
| 4 | History Lead | "My Votes" page — view, URL, template |
| 5 | QA / Frontend Lead | Bootstrap layout, integration tests, README, slides |

---

## Feature Status

| Feature | Status |
|---------|--------|
| User registration | ✅ Working |
| Login / Logout | ✅ Working |
| Bootstrap shared layout (`base.html`) | ✅ Working |
| Vote view (`@login_required`) | ⚠️ Login guard in place — choices not working |
| Personal Voting History ("My Votes") | ❌ Not implemented |
| Double-vote prevention (`UserVote` model) | ❌ Not implemented |


## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Baquatelle/uds-cc1-wup.git
cd uds-cc1-wup
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Visit https://baquatelle.pythonanywhere.com/polls/ — you will be redirected to `/polls/`.

---

## Running Tests

```bash
# Run all tests
python manage.py test polls

# Run auth tests only
python manage.py test polls.tests_auth

# Run with coverage report
coverage run manage.py test polls.tests_auth
coverage report
```

### Auth Tests (confirmed passing)

| Test | What it checks |
|------|----------------|
| `test_register_form_valid` | RegisterForm saves email as username |
| `test_registration_flow_redirects` | POST to /register/ creates user and redirects to polls index |
| `test_unauthenticated_user_cannot_vote` | Guest users redirected to /accounts/login/ |

---

## Git Workflow

- `master` is protected — no direct commits
- Every change: feature branch → commit → push → Pull Request → reviewer approval → merge
- Pull `master` into your branch daily
- Run `black .` before every commit
- Run `pytest` before every push — don't push red

### Commit message format

```
Add login template        ✅
Added login template      ❌
```

English, imperative mood, under 72 characters.

---

## Key URLs

| URL | Purpose |
|-----|---------|
| `/polls/` | Polls index (home page) |
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout |
| `/register/` | Registration page |
| `/admin/` | Django admin panel |

---

## Presentations

| When | What |
|------|------|
| Tue May 5, 2026 | Intermediate — topic, approach, plan |
| Tue May 12, 2026 | Final — live demo, results, lessons learned |

---

*Team Alfa - Coding Camp 1 - Warmup Project · May 2026*
