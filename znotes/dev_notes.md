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


---
# run commands

# 2026 10 14 Stack
mbpro:
Prev: Docker Desktop 4.89
Current: Docker Desktop 4.95.0

## requirements.txt
