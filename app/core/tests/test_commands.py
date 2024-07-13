"""
Test Django managememt command
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Pscop2gError
from django.core.management import call_command
from core.management.commands.wait_for_db import Command  # noqa
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for databse to be ready"""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database get operation error"""
        patched_check.side_effect = list(patched_check.side_effect)
        patched_check.side_effect = [Pscop2gError] * 2
        patched_check.side_effect += [OperationalError] * 3
        patched_check.side_effect += [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
