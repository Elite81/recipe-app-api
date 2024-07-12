'''
Test Django managememt command
'''

from unittest.mock import patch
from psycopg2 import OperationalError as Pscop2Error
from django.core.management import call_command
from core.management.commands.wait_for_db import Command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.handle')
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        '''Test waiting for databse to be ready '''
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default'])
