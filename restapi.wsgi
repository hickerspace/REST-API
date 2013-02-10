import sys
import os

#sys.path.insert(0, "/var/www/hickerspace.org/wsgi-scripts/restapi/")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from restapi import app as application
