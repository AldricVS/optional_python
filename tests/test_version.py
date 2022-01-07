import unittest

from optional_python import __version__

class ProjectDefinitionTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.1.0", "Version is not correct")