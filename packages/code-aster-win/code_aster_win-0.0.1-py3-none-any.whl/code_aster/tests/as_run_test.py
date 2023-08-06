import code_aster as ca
from pathlib import Path
from unittest import TestCase


class TestJoke(TestCase):
    def test_as_run(self):
        path = Path('code_aster/code-aster_v2019_std-win64/example/forma01a.export')
        logs = ca.as_run(path)
        print(logs)
        self.assertTrue(True)


