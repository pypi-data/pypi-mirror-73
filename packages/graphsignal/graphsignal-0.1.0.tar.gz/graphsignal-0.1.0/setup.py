import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'graphsignal',
  version = '0.1.0',
  description = 'Graphsignal',
  long_description = read('README.rst'),
  author = 'Graphsignal',
  author_email = 'devops@graphsignal.ai',
  url = 'https://graphsignal.ai',
  license = 'BSD',
  keywords = [],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: System :: Monitoring',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence'
  ],
  python_requires='>=2.7',
  install_requires=[],
  
  packages = find_packages(exclude=[
    '*_test.py', 'examples', 'scripts'])
)
