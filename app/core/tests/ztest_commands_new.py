"""
Test custom Django management commands.
"""

from unittest.mock import patch  # To Mock DB behaviour

from django.core.management import call_command  # call the custom command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg import (
    OperationalError as PsycopgOpError,
)


# Interceptamos el método ensure_connection de la base de datos por defecto de Django
@patch(
    "django.db.backends.base.base.BaseDatabaseWrapper.ensure_connection"
)
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_ensure_connection):
        """Test waiting for database if database ready.
        And that the custom command is ok and can be called"""
        # Al no lanzar errores, simulamos que la conexión física es exitosa inmediatamente
        patched_ensure_connection.return_value = True

        call_command("wait_for_db")

        # Verificamos que se intentó conectar exactamente una vez
        patched_ensure_connection.assert_called_once()

    @patch("time.sleep")  # Mock para que el test no espere segundos reales
    def test_wait_for_db_delay(self, patched_sleep, patched_ensure_connection):
        """Test waiting for database when getting OperationalError."""
        # Simulamos el ciclo de vida del primer arranque de Postgres:
        # 1 y 2: El puerto está cerrado (PsycopgOpError)
        # 3, 4 y 5: Está reiniciándose o inicializando tablas (OperationalError)
        # 6: Conexión exitosa (devuelve None/True de forma silenciosa)
        patched_ensure_connection.side_effect = (
            [PsycopgOpError] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        # Validamos que el comando insistió exactamente 6 veces antes de dar éxito
        self.assertEqual(
            patched_ensure_connection.call_count, 6
        )
