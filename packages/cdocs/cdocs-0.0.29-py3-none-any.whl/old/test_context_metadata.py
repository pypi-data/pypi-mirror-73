from cdocs.context_metadata import ContextMetadata
from cdocs.cdocs import Cdocs
import unittest

class ContextTests(unittest.TestCase):

    noise = False
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def test_metadata(self):
        self._print("ContextTests.test_roots")
        metadata = ContextMetadata()
        cdocs = Cdocs("")
        print("test!!!!!!!!!!!!!!!!!!!!!!!!!")

