# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

# from os.path import join, normpath
# from logging import Formatter, FileHandler
ALEXA_APP_ID = os.getenv('ALEXA_APP_ID')
DEBUG = False
# LOG_LEVEL = 'INFO'

# LOG_NAME = 'monzo.log'
# LOG_FOLDER = '/var/log/monzo/'
# LOG_PATH = normpath(join(LOG_FOLDER, LOG_NAME))


# FILE_HANDLER = FileHandler(filename=normpath(LOG_PATH))
# FILE_HANDLER.setLevel(LOG_LEVEL)
# FILE_HANDLER.setFormatter(Formatter(
#     '%(asctime)s %(levelname)s: %(message)s '
#     '[in %(pathname)s:%(lineno)d]'
# ))
