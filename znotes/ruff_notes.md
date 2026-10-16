# GEMINI RECO CONFIG FOR RUFF DJANGO 6 Python 3.14
For a cutting-edge stack utilizing Django 6 (6.0/6.1), Python 3.14, PostgreSQL 18, HTMX, and Tailwind CSS, your Ruff linting rules should be configured to enforce strict logic safety, take advantage of modern Python 3.14 idioms, protect Postgres/Gunicorn boundaries, and stay completely out of the way of your frontend pipeline (HTML/CSS). [1] (https://www.python.org/downloads/), [2] (https://endoflife.date/django), [3] (https://www.djangoproject.com/weblog/2026/aug/05/django-61-released/)
Here is the ideal production-ready pyproject.toml configuration containing the exact rule selections and overrides you should enforce:
```python
[tool.ruff]
target-version = "py314"  # Maximizes checks for Python 3.14 idioms
line-length = 88         # Standard formatting rule

[tool.ruff.lint]
# 1. Rules to Select
select = [
    "F",    # Pyflakes (Logic bugs, undefined variables)
    "E",    # Pycodestyle errors (PEP 8 layout compliance)
    "W",    # Pycodestyle warnings
    "I",    # Isort (Automated import sorting)
    "UP",   # Pyupgrade (Upgrades code to modern syntax up to Python 3.14)
    "B",    # Flake8-bugbear (Catches complex design flaws & pitfalls)
    "DJ",   # Flake8-django (Enforces strict Django best practices)
    "S",    # Flake8-bandit (Security testing - critical for Postgres/Gunicorn setups)
    "C4",   # Flake8-comprehensions (Enforces efficient list/dict comprehensions)
    "SIM",  # Flake8-simplify (Flags convoluted code logic)
    "ASYNC",# Flake8-async (Essential for Django 6 async query/pagination patterns)
    "T20",  # Flake8-print (Flags accidental 'print' statements left in code)
]

# 2. Rules to Ignore globally
ignore = [
    "E501",   # Line too long (Let the formatter handle line lengths automatically)
    "S101",   # Use of assert (Can cause false alarms if you use them heavily)
    "DJ012",  # Order of model inner classes (Sometimes too rigid for custom designs)
]

# 3. Context-Specific Project Overrides
[tool.ruff.lint.per-file-ignores]
# Allow necessary boilerplate and long auto-generated layout files in Django Migrations
"**/migrations/*" = ["E501", "RUF012"]

# Prevent test fixtures from complaining about security or mock constraints
"**/tests/*" = ["S101", "S105", "S106"]

# Django settings files need to handle raw string paths and variable names flexibly
"**/settings.py" = ["E501", "F403", "F405"]
```
Usa el código con precaución.

Why this specific rule selection matters for your environment:


1. DJ (Flake8-Django)

This rule set ensures you do not write outdated patterns. It will actively flag model fields lacking necessary defaults, discourage bad structure inside models, and keep database model relationships healthy before queries hit your PostgreSQL 18 wrapper layer.

2. ASYNC (Flake8-async)

Django 6 heavily highlights async enhancements, such as AsyncPaginator and async request handling via ASGI. This rule set protects you from writing standard blocking synchronous database blocks or bad coroutines that degrade performance behind your Gunicorn/Nginx routing layer. [1] (https://docs.djangoproject.com/en/6.1/releases/6.0/)

3. UP (Pyupgrade) configured for py314

Python 3.14 includes optimizations like zero-overhead debugging, deferred annotation evaluation (PEP 649), and standard library overhauls. Selecting UP tells Ruff to automatically upgrade older formatting types or outdated collections to native, highly performant syntax patterns. [1] (https://www.python.org/downloads/release/python-3140rc3/)

4. Keeping HTML/HTMX & Tailwind Clean

Ruff is strictly a Python engine linter. It will not touch or read your templates, leaving your HTMX attributes (hx-get, hx-target) and Tailwind class streams untouched.
• To ensure your workflow remains completely streamlined, make sure you configure your .dockerignore file to exclude your node pipelines (like node_modules/ or tailwind configuration output files) so they aren't parsed by backend tooling during container runtime routines (docker compose run --rm app ruff check .).
Would you like me to help you map out the matching Nginx configuration to route requests smoothly between your Gunicorn app server and your static Tailwind/HTMX assets?
