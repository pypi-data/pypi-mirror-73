#!/usr/bin/python
from distutils.core import setup

setup(name='PyPDB3',
      version='1.0',
      description='A parser for PDB files',
      long_description="""\
PyPDB : a python class to parse PDB files

Written (2001-2020) by P. Tuffery, INSERM, France

Contributions by R. Gautier, J. Maupetit, J. Herisson, C. Habib and others

This class is used in production since 2004 at the RPBS structural
bioinformatics platform. It relies on our strong experience in
biomolecular structure files.

""",
      author='P. Tuffery and J. Maupetit',
      author_email='pierre.tuffery@univ-paris-diderot.fr',
      url='http://bioserv.rpbs.univ-paris-diderot.fr',
      packages = ['PyPDB'],
      scripts = ['PDBToolbox'],
      classifiers=['License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      license='GNU General Public License (GPL)'
     )

