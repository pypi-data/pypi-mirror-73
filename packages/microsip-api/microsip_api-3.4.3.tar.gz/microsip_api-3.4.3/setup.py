import os
import compileall
import sys
from setuptools import setup, find_packages
import pathlib

if "sdist" in sys.argv:
    path = os.path.abspath(os.path.dirname(__file__))+"\\microsip_api\\"
    compileall.compile_dir(path, force=True)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.rst').read_text(encoding='utf-8')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='microsip_api',
    version='3.4.3',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='microsip api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Servicios de Ingenieria Computacional',
    author_email='desarrollo@siccomputacion.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
