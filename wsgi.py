#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/temperature/')
from temp_flask import app as application
application.secret_key = 'hot hot'
