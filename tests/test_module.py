import unittest

import stactools.aerial


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.aerial.__version__)
