from test_autogalaxy.integration.tests.imaging.galaxy_x1 import galaxy_light__hyper
from test_autogalaxy.integration.tests.imaging.runner import run_a_mock


class TestCase:
    def _test__galaxy_light__hyper(self):
        run_a_mock(galaxy_light__hyper)
