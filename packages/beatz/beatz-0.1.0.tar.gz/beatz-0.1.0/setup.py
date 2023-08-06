from setuptools import setup
from beatz.version import __version__

runtime = set([
    "youtube_dl==2020.6.16.1",
    "validators==0.15.0"
])

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='beatz',
    packages=['beatz'],
    url='https://github.com/yadneshk/beatz',
    install_requires=list(runtime),
    entry_points={'console_scripts': ['beatz=beatz.main:BeatzArguments']},
    author='yadneshk',
    author_email='yadnesh45@gmail.com',
    version=__version__,
    description='Download & stream music on your terminal'
)
