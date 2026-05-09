\# Django Polls — User Authentication + Personal Voting History



> Team Alfa - Coding Camp 1 - Warmup Project



An extension of the official Django tutorial polls app, adding full user

authentication and a personal voting history feature.



\---



\## What the app does



After our changes, users can:



\- Register an account, log in, and log out

\- Cast votes that are recorded against their account

\- View their personal voting history on a dedicated "My Votes" page

\- Be prevented from voting twice on the same poll — enforced at the database level



\---



\## Team



| # | Role | Responsibility |

|---|------|----------------|

| 1 | Auth Lead | Login, logout, and registration pages |

| 2 | Model Lead | UserVote model, migration, admin registration |

| 3 | Voting Lead | Securing vote() — login required, no double-voting |

| 4 | History Lead | "My Votes" page — view, URL, template |

| 5 | QA / Frontend Lead | Bootstrap layout, integration tests, README, slides |



\---



\## Setup



\### 1. Clone the repo



```bash

git clone https://github.com/Baquatelle/django-polls.git

cd django-polls/djangotutorial

```



\### 2. Create and activate virtual environment



```bash

python -m venv .venv

.venv\\Scripts\\activate        # Windows

source .venv/bin/activate     # Mac/Linux

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Run migrations



```bash

python manage.py migrate

```



\### 5. Start the server



```bash

python manage.py runserver

```



Visit http://127.0.0.1:8000/polls/



\---



\## Running the tests



```bash

python manage.py test polls.tests\_auth -v 2

```



\### Test coverage



```bash

pip install coverage

coverage run manage.py test polls.tests\_auth

coverage report

```



\*\*Current coverage: 95%\*\* (target: 80%)



| File | Coverage |

|------|----------|

| polls/forms.py | 100% |

| polls/views.py | 79% |

| polls/models.py | 84% |

| polls/tests\_auth.py | 100% |

| \*\*TOTAL\*\* | \*\*95%\*\* |



\---



\## Repository structure



| File / Folder | Purpose |

|---------------|---------|

| `README.md`, `requirements.txt`, `.gitignore` | Root configuration |

| `djangotutorial/manage.py` | Django CLI entry point |

| `djangotutorial/mysite/` | Project settings and root URLs |

| `djangotutorial/polls/` | The app — all feature work is here |

| `polls/forms.py` | RegisterForm — email as username |

| `polls/views.py` | register() view and vote() view |

| `polls/tests\_auth.py` | Full test suite (22 tests) |

| `polls/templates/` | HTML templates |

| `polls/migrations/` | Database schema changes |



\---



\## Git workflow



\- `master` branch is protected — no direct commits

\- Each feature lives on its own branch

\- Every change goes through a Pull Request with reviewer approval

\- `black` formatter run before every commit

\- `pytest` run before every push



\---



\*Team Alfa - Coding Camp 1 - Warmup Project · May 2026\*

