from setuptools import setup, find_packages
from os.path import join, dirname

import pynvg

__PACKAGE__='pynvg'
__DESCRIPTION__='pynvg is a general purpose library by NVG'
__VERSION__=pynvg.__version__

setup(
    name=__PACKAGE__,
    version=__VERSION__,
    packages=find_packages(include=__PACKAGE__),
    description=__DESCRIPTION__,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="lonagi",
    author_email='lonagi22@gmail.com',
    url="https://github.com/lonagi/pynvg",
)