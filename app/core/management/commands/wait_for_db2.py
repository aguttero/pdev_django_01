"""
Django command to wait for the database to be available.
"""

import time

from django.core.management.base import BaseCommand
from django.db import connections  # <--- Importación clave para probar la conexión real
from django.db.utils import OperationalError
from psycopg import OperationalError as PsycopgOpError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
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
