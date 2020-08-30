from breadbox import annotation_reader
from environ_vars import TKLIB_HOME
import unittest





class TestCase(unittest.TestCase):
    def dest_reader(self):
        annotations = annotation_reader.Annotations("%s/data/directions/breadbox/nouns_stefie10.txt" % TKLIB_HOME)
        self.assertEqual(len(annotations.data), 502)
        labels = set(["cell", "breadbox", "closet", "room", "house", "city", "universe", None])
        self.assertEqual(annotations.labels, labels)
