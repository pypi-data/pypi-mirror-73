# -*- coding: utf-8 -*-
"""

@author: Cayo Lopes
"""

from setuptools import setup, find_packages, Extension
import os

rootpath = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


with open('requirements.txt') as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='ecodatatk',
    version='0.0.1',
    include_package_data=True,
    pacotes=find_packages('src'),
    long_description=long_description,
    classifiers=['Development Status :: 1 - Planning',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Education',
                 ],
    url='https://github.com/cayolopesbc/eco-data-manage-toolkit',
    license='MIT License',
    author='Cayo Lopes B. Chalegre',
    author_email='cayo.chalegre@ufrgs.br',
    keywords='limnology hydrology spatial dataset',
    description='Developed for limnological and hydrological studies',
    install_requires=install_requires,
    packages=['ecodatatk'],
)