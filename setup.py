import sys
try:
    from setuptools.command.test import test as TestCommand
    from setuptools import setup
except ImportError:
    from distutils.core import setup

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

config = {
    'description': 'IOT Coop scripts',
    'author': 'Jimmy Puckett',
    'url': 'https://github.com/sjacres/iot-chicken-coop',
    'download_url': 'https://github.com/sjacres/iot-chicken-coop/archive/master.zip',
    'author_email': 'jimmy.puckett@spinen.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['coop'],
    'scripts': [],
    'name': 'Coop',
    'cmdclass': {'test': PyTest},
}

setup(**config)
