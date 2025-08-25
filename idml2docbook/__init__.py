import os
import sys
import logging
import contextlib

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

VERSION = __version__ = "0.4.2"

LOGGER = logging.basicConfig(filename='idml2docbook.log', encoding='utf-8', level=logging.DEBUG)