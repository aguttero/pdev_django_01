# Gemini info about drf-spectuacular 2026 10
drf-spectacular is the officially recommended, industry-standard library for generating OpenAPI 3.0 / 3.1+ schemas in modern Python web development. [1] (https://drf-spectacular.readthedocs.io/en/latest/readme.html), [2] (https://github.com/encode/django-rest-framework/discussions/8453)
If you are building a Django v6 REST API using Django REST Framework (DRF), it acts as the primary tool to automatically generate, host, and customize your API interactive documentation (such as Swagger UI or ReDoc). [1] (https://www.youtube.com/watch?v=E3LUvsPWLwM), [2] (https://www.reddit.com/r/django/comments/1kxf2n7/django_tip_automate_drf_api_documentation_using/)
Historically, developers used tools like drf-yasg, but those became obsolete because they were limited to the older OpenAPI 2.0 specification and lacked deep integration with modern DRF features. [1] (https://www.django-rest-framework.org/topics/documenting-your-api/)

Core Features

• Native OpenAPI 3.0+ Compliance: Fully supports complex types, structured payloads, and components. [1] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)
• Automatic Introspection: It reads your DRF serializers, viewsets, query parameters, validators, and authentication classes to generate a schema without you writing boilerplate. [1] (https://www.django-rest-framework.org/topics/documenting-your-api/), [2] (https://www.youtube.com/watch?v=E3LUvsPWLwM), [3] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)
• Granular Customization: Provides utility decorators like @extend_schema to explicitly type polymorphic payloads, custom exceptions, or metadata over individual endpoints. [1] (https://drf-spectacular.readthedocs.io/), [2] (https://python.plainenglish.io/drf-api-documentation-using-drf-spectacular-a-complete-guide-f7b94f1cf7d9), [3] (https://drf-spectacular.readthedocs.io/en/latest/drf_spectacular.html), [4] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)
• Code Generation Ready: The generated structured schema.yaml file can be fed straight into frontend client generators (e.g., generating TypeScript types or SDKs automatically). [1] (https://drf-spectacular.readthedocs.io/), [2] (https://www.youtube.com/watch?v=E3LUvsPWLwM)

Quick Implementation in Django v6

To configure drf-spectacular, follow these four quick setup steps: [1] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)

1. Installation

Install the package along with the optional interactive UI bundles and the offline "sidecar" (so your admin/documentation pages don't rely on external CDNs): [1] (https://python.plainenglish.io/drf-api-documentation-using-drf-spectacular-a-complete-guide-f7b94f1cf7d9), [2] (https://drf-spectacular.readthedocs.io/en/latest/readme.html), [3] (https://levelup.gitconnected.com/drf-spectacular-the-ultimate-tool-for-automated-drf-api-documentation-61bd4cca36b7)
bash
pip install drf-spectacular[swagger,redoc,sidecar]
Usa el código con precaución.

2. Settings Configuration (settings.py)

Register the apps and route DRF's default schema engine to use spectacular's inspector: [1] (https://levelup.gitconnected.com/drf-spectacular-the-ultimate-tool-for-automated-drf-api-documentation-61bd4cca36b7), [2] (https://www.youtube.com/watch?v=E3LUvsPWLwM), [3] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)
```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",  # Serves Swagger/ReDoc assets locally
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "My Modern Django v6 API",
    "DESCRIPTION": "Automated and rich documentation using drf-spectacular",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # Tells Swagger to use offline assets
    "REDOC_DIST": "SIDECAR",
}
```

3. Expose Documentation Routes (urls.py)

Import the spectacular views and map them to paths for the raw YAML/JSON schema, Swagger UI, and ReDoc interfaces: [1] (https://www.youtube.com/watch?v=KCyXZK0gEYs&t=194), [2] (https://www.youtube.com/watch?v=E3LUvsPWLwM)
Expose your schema and documentation views in your project's main urls.py by mapping endpoints for SpectacularAPIView, SpectacularSwaggerView, and SpectacularRedocView. [1] (https://www.youtube.com/watch?v=KCyXZK0gEYs&t=194), [2] (https://www.youtube.com/watch?v=E3LUvsPWLwM)

4. Fine-Tuning Endpoints (Example View)

To refine automated schemas or add specific metadata, use the @extend_schema decorator on your API views. [1] (https://python.plainenglish.io/drf-api-documentation-using-drf-spectacular-a-complete-guide-f7b94f1cf7d9), [2] (https://drf-spectacular.readthedocs.io/en/latest/readme.html)
Would you like assistance in customizing authentication schemes (e.g., JWT, OAuth2) for the Swagger dashboard, or do you need to handle polymorphic / conditional serializers with drf-spectacular?

# About SIDECAR and locally self-hosting ofr js and Css for swagger UI:

The drf-spectacular-sidecar package provides local, self-hosted static assets (JavaScript and CSS files) for Swagger UI and ReDoc directly from your Django application backend.
Instead of forcing a developer's or client's web browser to fetch files like swagger-ui-bundle.js from an external public content delivery network (CDN) like ://cloudflare.com or unpkg.com, the sidecar bundles these assets as standard Django static files.

Why You Should Avoid External CDNs for API Docs

Relying on external CDNs for internal developer tooling and API documentation introduces several vulnerabilities, operational roadblocks, and compliance risks.
Using the sidecar approach offers major architectural advantages:

1. Air-Gapped and Offline Environments

• The CDN Problem: If you are developing code on an airplane, in a secure facility, or on a local network with no active internet connection, the API documentation UI will fail to render because it cannot download the CDN files.
• The Sidecar Practice: The documentation works 100% offline on localhost. As long as your Django local development server runs, your documentation renders correctly.

2. Enhanced Enterprise Security & Privacy

• The CDN Problem: Modern web browsers send HTTP headers (like Referer) when requesting CDN files. This can leak private paths, enterprise domain names, or internal metadata to third-party CDN providers.
• The Sidecar Practice: Your data stays entirely within your infrastructure network boundary. No network calls ever leave the user's browser to an unvetted third party.

3. Strict CSP (Content Security Policy) Compliance

• The CDN Problem: Highly secure systems enforce strict Content Security Policies (CSP) that forbid the browser from executing scripts or styles from outside domains. To allow external CDNs, you have to open exceptions in your policy (e.g., adding script-src https://unpkg.com), which increases your attack surface.
• The Sidecar Practice: You can keep a tight, highly restrictive CSP (such as script-src 'self') because all JavaScript assets are originating from your own domain name.

4. Absolute Version Stability & Zero Breakage

• The CDN Problem: If an external CDN goes down, encounters a routing issue, or changes its asset delivery pathways, your API documentation breaks instantly without any changes to your code.
• The Sidecar Practice: Your documentation layout and rendering code are version-locked inside your codebase. The code only updates when you explicitly run a command like pip install --upgrade.
Would you like help setting up your Django environment variables to toggle between development asset hosting and production production pipelines (like AWS S3 or Whitenoise)?

# Non reliant on CDNs architecture
To serve the Swagger UI completely offline without relying on external CDNs in Django 6, Django REST Framework (DRF), and drf-spectacular, you need to download the Swagger UI assets (JS/CSS) locally and configure Django's static files system to serve them.
When running inside Docker, you must also ensure your Dockerfile or entrypoint script collects these static files so they are available to your web server (like Nginx) or local container environment.
Here is the complete step-by-step configuration:

## 1. Download the Swagger UI Assets Locally

Instead of pointing to unpkg or cdnjs, you will download the assets and put them into your Django project's static directory.
Create a folder structure inside one of your apps or your root static directory:
```bash
your_project/
├── static/
│   └── swagger-ui/
│       ├── swagger-ui-bundle.js
│       ├── swagger-ui-standalone-preset.js
│       └── swagger-ui.css
Usa el código con precaución.
You can download these files directly from the official Swagger UI GitHub Repository dist folder or via a package manager.
```

## 2. Configure settings.py

You need to tell drf-spectacular to look at your local static paths instead of the default remote URLs.
```python
# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Standard Django Static Files Configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure Django looks into your custom static directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 2. DRF Spectacular Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your API Documentation',
    'DESCRIPTION': 'API description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # --- OFFLINE/LOCAL SWAGGER UI CONFIGURATION ---
    # Points to your locally hosted bundle, preset, and stylesheet
    'SWAGGER_UI_DIST': '/static/swagger-ui', 
    'SWAGGER_UI_FAVICON_HREF': '/static/swagger-ui/favicon-32x32.png', # Optional
}
```

## 3. Update Docker Configuration

Because containers have isolated environments, you must run collectstatic during the build or container startup phase so Django aggregates the local Swagger UI files into your STATIC_ROOT.

### Option A: Run in Dockerfile (Recommended for Production)

If your static files are served by a reverse proxy like Nginx, compile them during the image build:

```ts
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
# Install dependencies including django, djangorestframework, drf-spectacular
# Note: Django 6 requires Python 3.10+
# For Django 6 compatibility, ensure you use the latest drf-spectacular release
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# Run collectstatic to move Swagger UI assets to your STATIC_ROOT
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Option B: Run via docker-compose Entrypoint (Recommended for Local Dev)

If you are developing locally and mapping a volume, run collectstatic when the container boots up:

```yaml
# docker-compose.yml
services:
  web:
    build: .
    command: >
      sh -c "python manage.py collectstatic --noinput &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"

volumes:
  static_volume:
```

## 4. Verify local asset loading

1. Fire up your Docker containers (docker compose up --build).
2. Navigate to your Swagger UI endpoint (e.g., http://localhost:8000/api/schema/swagger-ui/).
3. Open your browser's Developer Tools (F12) and go to the Network tab.
4. Refresh the page. You should see that swagger-ui-bundle.js and swagger-ui.css are loading directly from your local domain (/static/swagger-ui/...) with a 200 OK status, rather than initiating external network requests to external CDNs.
Are you setting this up for a local development environment using Django's built-in runserver, or do you need a production-ready setup with Nginx serving those static files out of a shared Docker volume?
