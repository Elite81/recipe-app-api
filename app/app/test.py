from . import calc
from django.test import SimpleTestCase

"""sample tests"""


class CalcTest(SimpleTestCase):
    """test the calc module"""

    def test_add_nmbers(self):
        """Test adding number together"""
        res = calc.add(68, 32)
        self.assertEqual(res, 100)

    def test_substract_number(self):
        """Test subtructing two number"""
        res = calc.subtrucat(7, 2)
        self.assertEqual(res, 5)
