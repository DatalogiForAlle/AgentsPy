import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Don't install PyQt dependencies on ReadTheDocs documentation builds

if os.getenv('READTHEDOCS'):
    install_requires = []
else:
    install_requires = [
        'PyQt5',
        'PyQtChart'
    ]

extras_require = {
    "tests": [
        "black",
    ],
    "docs": [
        "sphinx",
        "alabaster",
    ]
  }

extras_require["dev"] = extras_require["tests"] + extras_require["docs"]

setup(
  name='AgentsPy',
  packages=['agents'],
  version='0.8.1',
  license='gpl-3.0',
  description='Simple agent-based modeling library for python',
  long_description=long_description,
  author='Jens Kanstrup Larsen / Martin Dybdal',
  author_email='jkl@di.ku.dk',
  url='https://github.com/DatalogiForAlle/pyagents',
  download_url='https://github.com/DatalogiForAlle/AgentsPy/releases/tag/v0.1',
  keywords=['AGENT', 'MODELING', 'SIMULATION'],
  install_requires=install_requires,
  extras_require=extras_require,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
