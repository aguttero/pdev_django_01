# step by step setup 2026 10
## 1 Create Github Repo & link with local dev proj folder
## 2 Add Docker Hub Token to Github Repo
* hub.docker.com > login
  Profile icon > account settings
  Personal Access tokens > Generate New token -> Name it to identify it
  - Copy token
  - Copy username (docker login -u <username>)
* GitHub:
  Github project repo > settings > Secrets and Variables > Actions
  > New repository secret > Name: DOCKERHUB_USER / secret: dockerhub username > Add Secret
  > New repository secret > Name: DOCKERHUB_TOKEN / secret: dockerhub token -> Add Secret

  * To revoke access just delete the secret in github or the token in dockerhub
### permission level for docker hub access token
* R&W
Required for CI/CD pipelines that build, test, and push images. It allows GitHub to look up your existing images (Read) and upload newly built images (Write) to your repositories.
* Read-only
Used strictly for pulling images (e.g., if you only needed your EC2 instance to download images from a private repository without pushing anything back).

## 3 2026 10 dependencies (NO QUEUE BACKEND)
### django 5.2 LTS
Python 3.10 to 3.14
Postres 14+
  - psycopg or psycopg2
SQLite 3.27+ (no driver required)
WSGI
  - gunicorn, uWSGI

### PyMuPDF
Python: CPython 3.9 to 3.14
OS: macOS11+, Linux with glibc 2.17+ or Alpine 3.16+
256MB RAM // 60MB disk
#### Docker considerations
deploying to serverless platform (like AWS Lambda or Google Cloud Run) or using Docker, remember these constraints:
• Binary Size: Because the MuPDF C engine is compiled into the wheel, the binary package is relatively large. Watch your deployment bundle size limits.
• Threading Constraints: PyMuPDF does not support running on multiple threads and can crash if forced to do so. If your dashboard processes files asynchronously at scale, you must scale via Python’s multiprocessing library or a task worker queue like Celery instead of standard multithreading.

#### License open-source AGPL
You need to make the complete dashboard code open-source

### PyPDF
ZAG: need to test extraction
  
### django 6.1
Ptyhon 3.12 to 3.14
drf >=3.18
Postres 15+
  - psycopg (v3.1.2+) or psycopg2(v2.9.9+)
SQLite 3.37+ (no driver required)
Queue Backend for production

## 4 Requirements.txt
1. Start with: Django>=6.1,<6.2
2. Go to Dockerfile Creation below

### Req.txt v1 2026 10:
Django>=6.1,<6.2
djangorestframework>=3.18,<3.2
psycopg>=3.1.8,<3.2

  
## 5 Dockerfile
* Dockerfile - ZAG TEST (reco fallback: 3.14-slim)
choose base image: python:3.14.8-alpine 3.24
python is the name of the official image on docker hub 
3.14.8-alpine3.24 is the name of the tag

* This makes python output to print in console:
ENV PYTHONUNBUFFERED=1

* copies files, need to create dirs in local device first:
Sets pwd /app > this is where django project will reside
exposes port 8000 from container to machine
So we can connect to django web dev server
ZAG: remember to create app/ in the local project root
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

* run commands:
creates venv in /py; upgrades pip; installs requirements; deletes /tmp
best practice to create venv in docker as base python in image might conflict with app dependencies
adds user django-user to linux with no home folder and no password 
best practice not to user the root user

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
      --disabled-password \
      --no-create-home \
      django-user

* env config
updates the PATH environment variable inside the image
PATH defines all directories where executables can be run
this adds /py/bin to the system path
ENV PATH="/py/bin:$PATH"

* user selector
swithces from root user django-user
USER django-user

### dockerfile v1 2026 10
```dockerfile
FROM python:3.14.8-alpine3.24
LABEL maintainer="github.com/aguttero"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
```

## 6 add .dockerignore file
files we don't want to copy to docker image
```dockerignore
# Git
.git
.gitignore

# Docker
.docker

# Python
app/__pycache__/
app/*/__pycache__/
app/*/*/__pycache__/
app/*/*/*/__pycache__/
.env/
.venv/
venv/

# Other
.ruff_cache

```
## 6.5 add .venv and ruff to lint check locally
1. sh: python3 -m venv .venv
2. sh: pip install --upgrade pip
3. sh: pop install ruff

## 7 Test build image
1. cd to local project root folder
2. mkdir app (or the name of the app folder in the RUN section of dockerfile)
3. sh: docker build .
4. validate log ok. It creates image name 'none'
5. validate versions with docker desktop exec
  - docker image ls -a
  - docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
  - docker run --rm -it [image name] sh  
  - (--rm remove+volumes at end -i interactive -t allocate TTY sh command)
  - sh: ptyhon3 --version
  - sh: pip list
  - sh: printenv
  - sh: cat /etc/os-release
  ZAG: to login as root: (root is Uid 0 > -u 0)
  - docker run --rm -it -u 0 [image name] sh


## 8 Docker compose file v1 2026 10
1. create compose.yml in project root (docker-compose.yml in older versions)
Notes:
* args -DEV=true (for later use)
* ports: 8000:8000 puerto_host(local_dev):puerto_contenedor
* runserver 0.0.0.0:8000 > expone el 8000 del server
* volumes: ./app:/app host_path:container_path binding
 . dot de './app' = compose.yml folder 
* command: default command that will be run (can be overriden by docker-compose xxx -c "command")

2. Test it builds ok (same as in docker build but now it does it from docker compose and adds a tag name to image) 
  - in local project root: bash: docker compose build
3. To validate run: ('app' = service name in .yml file)  
  - as default user: sh: docker compose run --rm app sh
  - as root: sh: docker compose run --rm -u 0 app sh
  - validate bind in /app dir sh: mkdir tmp


### v1 compose.yml
```yml
services:
  app:
    build:
      context: .
      args:
        - DEV=true
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
```

## 9 Linting Setup
udemy 2021: flake8
2026 10: Ruff > faster, autofix (lits, formats, sort imports)
docs: https://docs.astral.sh/ruff/installation/
https://pypi.org/project/ruff/
https://pypi.org/project/ruff/#user-content-configuration
linting only installs in local dev container (does not go to prod deployment) > requirements.dev.txt
1. in local proj root create file: requirements.dev.txt
2. add build arg to docker compose:
  - args: - DEV=true
3. in dockerfile add copy lines, ARG and IF lines
  - COPY ./requirements.dev.txt /tmp/requirements.dev.txt
  - ARG DEV=false (which is overriden in docker compose local, by default we are not running dev mode)
  - add if dev=true in RUN commands
    ```sh  
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    ```
4. test image builds ok. From local proj root run:
  bash: docker compose build
  ZAG: image prev: 09ff2f4b530e 189.9MB
  ZAG: image after: 1b1364405a86 247MB
  Validate: bash: docker compose run --rm app sh
    - sh: ruff check [path]
  
5. Setup exclude folders for Ruff linting
  - Ruff config file (rules and excluded files)
  - create file:  local_project_root/app/ruff.toml
  - add django folders and files to exclude
  ```python
    extend-exclude = [
        "migrations",
        "__pycache__",
        "manage.py",
        "settings.py",
        ]
  ```
6. Test run in container:
  - bash: docker compose run --rm app sh -c "ruff check" (this opens container runs shows report and exit) > All Checks passed!
  - bash: docker compose run --rm app sh
    - sh: ruff check [path] (this allows you to stay in the container shell until you type exit)


### how to run ruff:
1. open container shell
bash: docker compose run --rm app sh
2. to check > sh: ruff check [path]
3. to fix > sh: ruff check --fix
4. to format > ruff format

### simple error fix
- templfate files exclusions, line level **add #noqa**
- trailing white spacees: configure editor to **Remove trailing whitespace on save**

### how to setup exclusions in ruff.toml file
if you want to keep Ruff's built-in defaults (which automatically handle .git, .venv, __pycache__, etc.) but add extra rules, always use extend-exclude instead. This prevents your custom list from accidentally wiping out Ruff's smart defaults:
```python
# ruff.toml

# Merges your custom paths with Ruff's default ignore list
extend-exclude = [
    "custom_compiled_folder/", (or "custom_compiled_folder")
    "build/", (or "build")
]
```

#### option 1 complete exclude
* To avoid Ruff to touch, check, or format your files at all, add the wildcard pattern to the global exclude array at the top level of your ruff.toml:
```python
# ruff.toml
exclude = [
    "**/migrations/*.py", ZAG: this notation excludes files individually
]
```
* If you run Ruff via pre-commit hooks, pre-commit explicitly overrides default exclude rules by passing file names directly. To force Ruff to respect your exclusions during pre-commit, you must also add force-exclude = true:
```python
# ruff.toml
exclude = [
    "**/migrations/*.py",
]
force-exclude = true
```
#### option 2 - Ignore Linting, keep formatting
* Often, developers prefer to let Ruff format the files (ruff format) to keep whitespace clean, but want to ignore lint rules (ruff check) so that auto-generated code doesn't throw error
To bypass all linter warnings for folder 'migrations', use per-file-ignores inside the [lint] block
```python
# ruff.toml

[lint]
# Ignore ALL rules ("ALL") for any file inside a migrations folder
per-file-ignores = { "**/migrations/*.py" = ["ALL"] }
```
ZAG PENDING: find out how to ignore multiple individual files and how to specify this in the toml file

### requirements.dev.txt file v1 2026 10
ruff>=0.17.1,<0.20


### dockerfile v1.1 
```ts
FROM python:3.14.8-alpine3.24
LABEL maintainer="github.com/aguttero"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
```

## 10 Create Django Project inside Docker
1. in local sh: docker compose run --rm app sh -c "django-admin startproject app ." (app is the django proj name)
   ZAG: named 'dapp' wiht this command: sh: docker compose run --rm app sh -c "django-admin startproject dshbrd ."
2. test django dev server in localhost:8000
   local sh: docker compose up (this runs command line in compose.yml > sh -c "python manage.py runserver 0.0.0.0:8000")
   sh: docker compose down to end or ctrl+c

### naming best practice for django app
Name your Django project directory after the actual name of your application (e.g., myproject, ecom_backend, portfolio), while keeping the Docker root directory generic if you want.
For example, if your product is called "Nimbus", run this instead:
sh:  docker compose run --rm app sh -c "django-admin startproject nimbus ."

Resulting structure:
app/                 <-- Docker working directory
├── manage.py
└── nimbus/          <-- Clear Django project configuration folder
    ├── settings.py
    └── urls.py

## 11 GitHub actions configuration
1. Action file > in proj root > create file: .github/workflows/checks.yml (can be [any_file_name.yml])
  - This file automates:
    - Triggers
    - Code Linting
    - Unit Testing
  - Add three --- at beginning of file (this means is .yml file)
  - on: section > This is the trigger
    - on: [push] > this triggers on every push
    - on: 
        workflow_dispatch: > this allows to manually trigger from GitHub 
    - runs-on [ZAG 2026 10]:ubuntu-24.04 (check for less expensive linux runner if running on Github paid, this runner already has docker and docker-compose installed) [ZAG NOTE: user Docker Buildx setp for more complex and faster action automation. order: 1.login 2.Buildx. 3 run actions]
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
    
    - steps:
        - name: Login to Docker Hub
          uses: docker/login-action@v4 [ZAG 2026 10]
          with: 
            username, password > secret token
        - name: Checkout code [there might be steps that don't require checkout]
          uses: actions/checkout@v4
        - name: Test
          run:[v1] docker compose run --rm app sh -c "python manage.py test"
        - name: Lint
          run:[v2] docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"
        - name: Ruff Linter
          ZAG: THIS TESTED OK > # Force the container process to match the runner's user permission
          run: docker compose run --rm --user "$(id -u):$(id -g)" app sh -c "ruff check"
          ZAG: Test did not work
          run: docker compose run --rm app sh -c "ruff check --cache-dir /tmp/ruff_cache" (ZAG added --cache-dir to avoid permissions os error 13)
        

        
  - PUSH to GITHUB in order to create the action
2. Set Docker Hub Authentication (to have higher rate limits 200pulls/6h) per ip address > done in ## 2
3. Crate Secrets in GitHub Project wiht docker hub credentials > done in ## 2

3. Validate actions in GitHub
  - After commit and push the checks.yml file
  - Go to Gihub repo > actions
    - if trigger: push should be running
    - if trigger manual: trigger to test.

## 12 TDD Test Driven Dev
1. create tests/ folder, add __init__.py file
2. Or create file tests.py in main app folder
3. test modules start with 'test_'*.py
4. setup test DB (django creates it automatically)
  - django clears DB after each individual test (can be overriden for test data sets)
5. Django test clases:
  - SimpleTestCase (no DB integration)
  - TestCase (DB integration) 
  - To setup a test import TestClass + Code module to Test
  ```python
from django.test import SimpleTestCase
from django.test import TestCase
from subapp import views (where code to test resides)
```

### Test for health-check api

## 13 Configure DB - Postgres
### PostgreSQL + Docker Compose - Arquitecture features
- DB config defined un project code (re-usable for other devs and prod env)
- Persistent data in docker volumes
- Handles Network config
- Handles env variable configuration

#### Postgres 18 Database Cluster path
https://www.postgresql.org/docs/18/creating-cluster.html

#### Services in docker compose 
app: depends_on: - db
db: 
  image: postgres:18-alpine3.24
  volume: dev-db-data:/var/lib/postgresql [ZAG 2026 - docker hub docs]

### 1. configure docker-compose.yml
#### compose.yml dev v2
```yml
services:
  app:
    build:
      context: .
      args:
        - DEV=true
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
    environment:
      - DB_HOST=db
      - DB_NAME=devdb
      - DB_USER=devuser
      - DB_PASS=changeme
    depends_on:
     - db

  db:
    image: postgres:18-alpine3.24
    volumes:
      - dev-db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=devdb
      - POSTGRES_USER=devuser
      - POSTGRES_PASSWORD=changeme

    # healthcheck:
    #  test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
    #  interval: 5s
    #  timeout: 5s
    #  retries: 5s

volumes:
  dev-db-data:
```
### 2. Validate: 
  - sh: docker compose up > should see db and app services in console log
  - sh: docker compose ps > check status 
  - sh: docker inspect pdev_django_01-db-1
  - sh: docker inspect pdev_django_01-db-1 --format='{{json .State}}'
  - sh: docker inspect pdev_django_01-db-1 --type "container"

### 3. Install db adaptor dependencies
### psycopg documentation
https://pypi.org/project/psycopg/ v 3.3.6 [2026 10]
https://www.psycopg.org/psycopg3/docs/basic/install.html#

#### 1 dockerfile v2
FROM python:3.14.8-alpine3.24
LABEL maintainer="github.com/aguttero"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        gcc musl-dev postgresql-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

#### djagngo db dev env config
* psycopg compiles from source os, so requires dependencies in docker linux before installing with pip install
* psyscopg[binary] > good for dev (precompiled) avoid for production
* psycopg[c] > Builds C extensions from source, requires libpq + build tools
  - Requisites:
    - C Compiler
    - python3-dev (python dev headers)
    - libpq-dev (PostgreSQL client dev headers)
    - pg_config program available in PATH
  - pip install > sh: pip install "psycopg[c]"
* to add packages in alpine need to use alpine package manager 'apk'
  - gcc (GNU Compiler Collection) = C Compiler
  - musl-dev (Standard C Library Headers) replaces: glibc (core C library)
  - postgresql-dev (postgres Client dev files) provides libpq header files anad libraries. (internal C functions for raw networks sockets, parse queries and receive data streams from PSQL DB server)
 * Best practice: add these packages to build and then delete them
  
##### Psycopg compiling notes (gemini)
Because you are explicitly using an Alpine-based Python image (alpine3.24), building Python packages like psycopg (the database adapter Django uses) requires compiled C binaries. In your Dockerfile, make sure you install musl-dev, gcc, and postgresql-dev packages before running your pip install loop to prevent build failures.

##### from udemy for psycopg2 (older)
  - alpine equivalents:
  - postgresql-client (command line tools psql (sql shell), pg_dump, pg_restore and others)(allows manually run SQL queries and backup/restorecommands from terminal and wait-for-postgres script before python manage.py runserver or migrate execution)
  - build-base (gemini says it is not needed)
  - postgresql-dev
  - musl-dev

### 4. Update python reqs.txt 
[2026 10] add psycopg[c]>=3.3.6,<3.4
#### requirements.txt:
Django>=6.1,<6.2
psycopg[c]>=3.3.6,<3.4

### 5 build and test
- sh: docker compose down (in case a container is running)
- sh: docker compose build (check for errors)
- sh: docker compose run --rm app sh (pip list > psycopg-c)
- docker desktop > exec in db-1 sh: pg_isready
- sh: docker compose up > docker ps > docker exec -it [container_name_or_id] sh > pg_isready

### 6. configure django (engine, hostname, port, db name, username, pwd)
* settings.py
1.DATABASES: Remove sqlite3, add postgres, add env var, add import os
  - add import os
  - add 'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
  - the env var names need to be exact match those in docker compose file
  - remove db.sqlite3 file from app/ folder and git tracking

### 7. Fix DB race condition
- Create Django custom command 'wait for db'
1. Create django app 'core'
  - docker compose run --rm app sh -c "python manage.py startapp core"
  - clean files : tests.py, create tests/ add tests/__init__.py
  - add 'core' to installed apps in settings.py
  - create core/management/commands/wait_for_db.py (and __init__.py in all folders)
  - create test for wait_for_db in core/tests/test_commands.py
  - test with: docker compose run --rm app sh -c "python manage.py test"
2. Add wait_for_db to:
  - .github/workflows/checks.yml (see #8.2)
  - compose.yml > commands (see #8.1)

#### ZAG. WARNING - APP error during first DB startup
*  The docker app will fail the first time that Postgres needs to create the DB structure for the first time.
  - The DB starts and Stops and Restars when setting up for first time
* Run docker compose down and docker compose up again. This should fix the issue

##### FIX wait for actual ORM connection
¿Qué cambió y por qué soluciona el problema?

1. from django.db import connections: En lugar de usar self.check(), que evalúa configuraciones a nivel de la app de Django, traemos las conexiones internas del ORM.
2. db_conn.ensure_connection(): Este método le dice a Django: "Abre el socket e intenta comunicarte con el motor de base de datos". Si Postgres está en la fase de "apagado y reinicio" de su primer arranque, la conexión física fallará legítimamente y lanzará una excepción. El bucle while capturará el error, esperará un segundo más y volverá a intentarlo hasta que el reinicio definitivo de Postgres concluya por completo.

##### FIX CODE
```python
"""
Django command to wait for the database to be available.
"""

import time

from django.core.management.base import BaseCommand
from django.db import connections  # <--- Importación clave para probar la conexión real
from django.db.utils import OperationalError # django error DB not ready
from psycopg import OperationalError as PsycopgOpError # python error renamed to avoid confusion with django error


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
         # stdout -> prints to console
        self.stdout.write("Waiting for database...")
        db_up = False

        while db_up is False:
            try:
                # 1. Obtenemos el wrapper de la base de datos por defecto
                db_conn = connections["default"]

                # 2. Forzamos a Django a abrir una conexión física real y ejecutar un comando ping
                db_conn.ensure_connection()

                # Si llega aquí, la conexión es robusta y real
                db_up = True
            except (PsycopgOpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
```
##### FIX TEST CODE
**ZAG PENDING** Both tests fail:
django.test.testcases.DatabaseOperationForbidden: Database threaded connections to 'default' are not allowed in SimpleTestCase subclasses. Either subclass TestCase or TransactionTestCase to ensure proper test isolation or add 'default' to core.tests.test_commands.CommandTests.databases to silence this failure.

Qué cambió exactamente en el test?

1. La ruta del @patch principal:
	• Antes: "core.management.commands.wait_for_db.Command.check"
	• Ahora: "django.db.backends.base.base.BaseDatabaseWrapper.ensure_connection"
	• Por qué: Como cambiamos el código de la aplicación para usar el manejador de conexiones internas de Django, ahora interceptamos directamente la raíz de donde Django levanta los sockets hacia Postgres.
2. assert_called_once() en lugar de assert_called_once_with(...):
	• El método ensure_connection() no recibe el parámetro databases=["default"] (eso se decide antes, al elegir el diccionario en connections["default"]). Por ende, simplemente comprobamos que el método se haya ejecutado (assert_called_once()).
3. El comportamiento de side_effect:
	• Sigue funcionando exactamente igual de genial. Simula tus 2 caídas de puerto, tus 3 errores de inicialización de Postgres, y el éxito final al sexto intento, asegurando que tu lógica de reintentos sea a prueba de balas contra ese reinicio fantasma del contenedor.

### 8. Set up Database Migrations  
* command to prepare migrations: (after data model modification)
  - sh: python manage.py makemigrations 

* command to execute migrations:
  - sh: python manage.py migrate
  - best practice: automate run migrate command after wait for db every time you start django

#### 1 Edit compose.yml > COMMAND
add wait for db and migrate commands
```.yml
command: >
      sh -c "python manage.py wait_for_db &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
```
#### 2 Edit .github/workflows/checks.yml
```.yml
      - name: Test
        run: docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"
```

#### 3 can test and then delete DB volume to reset before changing user_model to email instead of user_id
* ZAG: Wait to change Custom user model first (## 9) as initial migrations will setup the std django user model
sh: docker compose up
check for wait for db command and migrations

## 14. Set up Custom user model (change user_id to email)
If you are implementing this in an existing project where migrations have already been run, switching the AUTH_USER_MODEL can cause database conflicts. **It is heavily recommended to set up a custom user model at the very beginning of a Django project.**

* Create model (Base from AbstracBaseUser + PermissionMixin)
* Create custom user manager (Used for CLI integraiont)
* Set AUTH_USER_MODEL in settings.py
* Manually Delete DB volume if started with standard django user model
* Create and run migrations

### 1 Design
Data Model
- email (EmailField)
- name (CharField)
- is_active (BooleanField)
- is_staff (BooleanField) > To determine is they can login to the Django admin

Hashing password method?

### 2 Code
* core/tests/test_models.py > add unittest
* use normalize_email(email) to avoid duplicates
* core/models.py > create custom user model + user manager
- in class User:
    objects = UserManager () binds User class with User Manager
    USERNAME_FIELD = "email" > tells django to use this instead of username_id
- in class UserManager override:
    def create_user
    def create_superuser
    note: create_user(password=None) is the default django behaviour (For use case where you need a passwordless user that can't login to the console)
* settings.py > 
  - add at bottom of file: 
    AUTH_USER_MODEL = 'your_app_name.User'
    AUTH_USER_MODEL = 'core.User'

### 3 make migrations
1. Make migrations
sh: docker compose run --rm app sh -c "python manage.py makemigrations"
validate: core/migrations/0001_initial.py
2. Migrate
sh: docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
error: inconsistent migration history  > This happens if data model previuosly initialized 
To fix:
  > manually delete the dev-db-data volume
  > alt 1: docker desktop
  > alt 2: docker volume ls > look for db volume name [proj_name_dev-db-data]
    sh: docker volume rm [volume_name]
    id volume in use > sh: docker compose down and retry volume rm
  > run again: docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate" > if fails, is because of the temporary postgres server for the very first time, run again and it works.
3. ZAG: Going back to (## 13.7)FIX DB RACE CONDITION to fix the code.
  - instead of waiting for a self.check = ok will wait for an ORM OK

### 4 Create SuperUser
1. open localhost:8000/admin
2. create super user > sh: docker compose run --rm app sh -c "python manage.py createsuperuser" 
3. (email -> admin@example.com / pass -> p underscore 123)
4. If you forget user, need to clear DB or run createsuperuser
5. Test login in localhost:8000/admin

## 15. Setup Django admin
1. customize the admin or add user page if needed
2. tdd in core/tests/test_admin.py
3. Code core/admin.py
```python
#bare min code to test in 8000/admin
"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ("id",)
    list_display = ("email", "name",)

admin.site.register(models.User, UserAdmin)
```
4. Validate in unittest and localhost:8000/admin (/change page should fail until fieldset is defined) 
- fieldset should only include fields that are in our data model

## 16. API Setup
### 1 Automated API documentation Setup
1. install drf-spectacular > requirements.txt drf-spectacular >=0.30.0,<0.31
- ZAG this installs djangorestframework 3.18.3 and others
SIDECAR?
2. re build container > docker compose build
3. valdiate with pip list in py venv in docker container
4. in settings.py add 
  - installed apps: 'rest_framework', 'drf_spectacular'
  - bottom of file > REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'}
  - > SPECTACULAR_SETTINGS = {'COMPONENT_SPLIT_REQUEST': True,}
5. enable URLs > app/dshbrd/urls.py (urlpatterns + imports)
```python 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# for health check api
from core import views as core_views
# add to ulrpatterns list:
path('api/health-check/', core_views.health_check, name='health-check'),
path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),name='api-docs'),

```

6. create core/views.py:
```python
"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
```

7. TEST 
  - localhost:8000/api/docs
  - localhost:8000/api/health-check/

#### ZAG Pending: 
- Swagger UI non-reliant on externa CDN config
- Redocs implementation


### 2. Build USER API
#### API functions:
- User registration
- Creating Auth Token
- Viewing/updating profile

#### endpoints
- user/create
  - POST register new user
- user/token
  - POST > new token (receives userid and pwd returns token )
- user/me
  - PUT/PATCH - update user profile
  - GET - retrieve user profile

#### Code
1. create app user from proj root > sh: docker compose run --rm app sh -c "python manage.py startapp user"
2. clean up files
  - migrations > all migrations consolidated in core app
  - admin > idem
  - models > idem
  - tests > create subfolder tests/ (remember to add __init__.py)
3. in app/settings.py
  - add user app to INSTALLED APPS
4. TDD > create user/tests/test_user_api.py
5. Test TDD > docker compose run --rm app sh -c "python manage.py test"
6. add Serializer for User Object > user/serializer.py > min pass lenght
  - serializer convert and validate web objects (json) to python or DB objects
  - ZAG: RUFF 012 error -> Add ClassVar annotation or add > # noqa: RUF012 supresses the mutable class attribute waring
  ```python
  from typing import ClassVar
  class UserSerializer(serializers.ModelSerializer):
      """Serializer for the user object."""
  
      class Meta:
          model = get_user_model()
          # noqa: RUF012 suppresses the mutable class attribute warning
          fields = ("email", "password", "name")  # Changing to tuple is still best practice
          extra_kwargs = {  # noqa: RUF012
              "password": {"write_only": True, "min_length": 5}
          }
```
7. add views for User Serializer > user/views.py
  - ZAG PENDNG: review revoketoken process for an admin (now is for self user)
  - see notes in lrn_django_api notes.md line #874
8. add urls to user/urls.py
9. include urls in dshbrd/urls.py
10. Authentication: Token API
11. in settings.py add installed apps: 'rest_framework.authtoken'
12. stop django if running and restart to allow for rest_fram.authtoken to execute migrations 
13. Test in browser api/docs/ and /admin > create token for user > authorize token xxxxxx
14. fix error core/views.py [health_check]: unable to guess serialzer

#### 14. fix error core/views.py [health_check]: unable to guess serialzer
This is a warning generated by a documentation tool like drf-spectacular or drf-yasg while it is auto-generating your OpenAPI/Swagger schema.

The tool is warning you that because your health_check view uses a basic @api_view decorator and returns a raw dictionary, it doesn't know what data structure the endpoint returns to document it properly.

##### fix: Use @extend_schema to document it inline (Recommended)

If you are using drf-spectacular, you can import the @extend_schema decorator to tell the schema generator exactly what type of response to expect, completely silencing the warning.
```python
"""
Core views for app.
"""
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse # fix guess serializer

@extend_schema(
    responses={
        200: OpenApiResponse(
            description="API is healthy",
            response={'type': 'object', 'properties': {'healthy': {'type': 'boolean'}}}
        )
    }
)
@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
```




---
# Django Security
ZAG: Read docs and tutorials:
https://docs.djangoproject.com/en/6.1/topics/security/
ZAG: Pending -> define type of authentication
  Token
  JWT
  Session

# run commands

# 2026 10 14 Stack
mbpro:
Prev: Docker Desktop 4.89
Current: Docker Desktop 4.95.0

## requirements.txt
