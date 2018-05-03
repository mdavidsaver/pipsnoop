
import unittest

class TestDTest(unittest.TestCase):
    def test_dtest(self):
        import dtest
        self.assertEqual(dtest.foo(), 42)
