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
1. Starti with: Django>=6.1,<6.2
2. Go to Dockerfile Creation below

10: final Req.txt:
Django>=6.1,<6.2
djangorestframework>=3.18,<3.2
psycopg>=3.1.8,<3.2

  
## 5 Dockerfile, .gitignore .dockerignore
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
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

* run commands:
creates venv and upgrades pip

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \


### V1 dockerfile:
FROM python:3.14.8-alpine 3.24
LABEL maintainer="github.com/aguttero"



### dockerfile 2026 10



1. create Dockerfile in project root

# run commands

# 2026 10 14 Stack
Docker Desktop 4.95.0

## requirements.txt



## Dockerfile
FROM python:3.9-alpine3.13
LABEL mantainer="github.com/aguttero"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000
