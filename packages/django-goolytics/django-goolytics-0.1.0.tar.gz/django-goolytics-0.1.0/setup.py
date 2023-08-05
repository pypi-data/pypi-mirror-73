from setuptools import setup

setup(
   name='django-goolytics',
   version='0.1.0',
   author='SJ',
   author_email='sheldonj22@gmail.com',
   packages=['goolytics'],
   scripts=['bin/goolytic-setup.bat'],
   url='http://pypi.python.org/pypi/django-goolytics/',
   license='LICENSE',
   install_requires=[
       "Django >= 3.0.0",
   ],
)