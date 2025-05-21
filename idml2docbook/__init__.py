import os
import sys
import logging
import contextlib
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

VERSION = __version__ = "0.1.0"

IDML2HUBXML_OUTPUT = os.getenv("IDML2HUBXML_OUTPUT_FOLDER") if os.getenv("IDML2HUBXML_OUTPUT_FOLDER") else "idml2hubxml"

DEFAULT_OPTIONS = {
    'idml2hubxml_file': False,
    'map': os.getenv("MAP"),
    'empty': False,
    'hierarchy': False,
    'cut': False,
    'names': False,
    'typography': False,
    'linebreaks': False,
    'prettify': False,
    'media': "Links",
    'raster': None,
    'vector': None,
    'idml2hubxml_output': IDML2HUBXML_OUTPUT,
    'idml2hubxml_script': os.getenv("IDML2HUBXML_SCRIPT_FOLDER"),
}

LOGGER = logging.basicConfig(filename='idml2docbook.log', encoding='utf-8', level=logging.DEBUG)