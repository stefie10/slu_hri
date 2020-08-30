
import unittest
from PyQt4.QtCore import *
from qt_utils import convertVariant

class AcrossTestCase(unittest.TestCase):
    def testConvertVariant(self):
        self.assertEqual(convertVariant(QVariant(True)), True)
        self.assertEqual(convertVariant(QVariant("Hi")), "Hi")
        self.assertEqual(convertVariant(QVariant("Hi")).__class__, "Hi".__class__)
        
