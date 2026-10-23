# 2026 10 Gemini Reverse URL notes for admin pages
El código para revertir la URL de la página de administración sigue siendo el mismo en Django v6, pero con una sutil e importante actualización en las buenas prácticas de importación:
```python
from django.urls import reverse

# Código completamente válido y moderno para Django v6:
url = reverse("admin:core_user_changelist")
```

El patrón de nombres "admin:<app_label>_<model_name>_changelist" es un estándar de diseño interno de Django que se mantiene idéntico. 

Lo que sí debes actualizar si vienes de un proyecto muy antiguo (o si quieres blindar el test para el futuro) son los siguientes detalles: [1] (https://www.ianlewis.org/en/reversing-django-admin-urls)

## 1. Asegura la importación moderna

Si el test original de Django v3 importaba reverse desde el antiguo módulo django.core.urlresolvers (deprecado hace tiempo), debes asegurarte de importarlo desde el módulo moderno: [1] (https://stackoverflow.com/questions/5680405/override-django-admin-urls-for-specific-model), [2] (https://stackoverflow.com/questions/74269899/reversing-admin-change-url)
```python
# CORRECTO (Django v4, v5 y v6):
from django.urls import reverse
Usa el código con precaución.
```

## 2. Hazlo dinámico (Recomendado para tests robustos)

En lugar de escribir en texto plano ("core_user"), la mejor práctica moderna en Django v6 para evitar fallos si cambias el nombre del modelo o la app es construir el string utilizando la metadata del modelo (_meta): [1] (https://books.agiliq.com/projects/django-admin-cookbook/en/latest/object_url.html), [2] (https://forum.djangoproject.com/t/reverse-admin-urls/41535)
```python
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Genera dinámicamente "admin:core_user_changelist"
url = reverse(f"admin:{User._meta.app_label}_{User._meta.model_name}_changelist")
```

## WARNING: 
El único cambio real que podría romper tu test en Django v6
**El nombre del espacio de nombres de la administración (admin:) depende directamente de cómo esté incluido en tu archivo principal urls.py.**
Asegúrate de que en tus rutas principales lo tengas declarado de la forma estándar moderna utilizando path(): [1] (https://www.w3schools.com/django/django_admin.php), [2] (https://stackoverflow.com/questions/74269899/reversing-admin-change-url)
```python
# urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),  # <--- Esto habilita automáticamente el namespace 'admin'
]
```

Si el test te está fallando o arrojando un error tipo NoReverseMatch, indícame:
• El error exacto que arroja la consola.
• Cómo tienes declarada la ruta de admin en tu urls.py.
¡Lo revisamos de inmediato para dejarlo funcionando!
