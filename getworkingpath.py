"""
Denne kan du bruke for å få tilgang til eksterne filer i python
Husk at getworkingpath.py må ligge i samme katalog som programmet ditt
Bytt ut filnavn.txt med den filen du skal bruke


Kode:

from getworkingpath import *

filnavn=getworkingpath()+"/filnavn.txt"

"""

import sys, os

def getworkingpath():          
    pathname = os.path.dirname(sys.argv[0])    
    return os.path.abspath(pathname)