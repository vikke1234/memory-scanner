from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension
from glob import glob

scanner_module = Pybind11Extension("memory",
                                   sorted(glob("src/c_extensions/*.cpp")))
setup(
    name='ot',
    version='0.0.1',
    packages=[''],
    url='',
    license='GPLv3',
    author='Viktor Horsmanheimo',
    author_email='viktor.horsmanheimo@helsinki.fi',
    description='memory scanner',
    ext_modules=[scanner_module]
)
