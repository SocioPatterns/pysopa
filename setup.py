#!/usr/bin/env python
#
#  Copyright (C) 2008-2010 Istituto per l'Interscambio Scientifico I.S.I.
#  You can contact us by email (isi@isi.it) or write to:
#  ISI Foundation, Viale S. Severo 65, 10133 Torino, Italy. 
#
#  This program was written by Ciro Cattuto <ciro.cattuto@gmail.com>
#

#from distutils.core import setup, Extension
from setuptools import setup, Extension

setup (name = 'sociopatterns',
    version = '0.1',
    description = 'SocioPatterns Python analysis framework',
    url = 'http://www.sociopatterns.org/',
    packages = ['sociopatterns'],
    ext_modules = [ Extension('sociopatterns.xxtea', sources = ['src/xxtea.c']) ],
    )

