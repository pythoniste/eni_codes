import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'psycopg2',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='contact',
      version='0.0',
      description='contact',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      message_extractors = { '.': [
          ('**.py',   'lingua_python', None ),
          ('**.pt',   'lingua_xml', None ),
          ]},
      test_suite='contact',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = contact:main
      [console_scripts]
      initialize_contact_db = contact.scripts.initializedb:main
      show_settings = contact.scripts.settings:main
      contact = contact.scripts.contact:main
      gcontact = contact.scripts.gtk:main
      """,
      )
