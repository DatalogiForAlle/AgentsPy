from distutils.core import setup
setup(
  name='agentspy',
  packages=['agentspy'],
  version='0.1',
  license='gpl-3.0',
  description='Simple agent-based modeling library for python',
  author='Jens Kanstrup Larsen / Martin Dybdal',
  author_email='jkl@di.ku.dk',
  url='https://github.com/DatalogiForAlle/pyagents',
  download_url='https://github.com/DatalogiForAlle/AgentsPy/releases/tag/v0.1',
  keywords=['AGENT', 'MODELING', 'SIMULATION'],
  install_requires=[
          'PyQt5'
      ],
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
