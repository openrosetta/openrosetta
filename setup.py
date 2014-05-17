""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(name='openrosetta',
      version=0.1,
      description='openrosetta',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=[
          'webtest',
          'nose'],
      install_requires=[
          'cornice',
          'waitress',
          'ming',
          'colander==1.0b1',
          'xlrd'],
      entry_points="""\
      [paste.app_factory]
      main = openrosetta:main
      """,
      paster_plugins=['pyramid'],
)
