import os
import sys
import logging
import contextlib
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

VERSION = __version__ = "0.1.0"

def getEnvOrDefault(envConst, default=False):
    return os.getenv(envConst) if os.getenv(envConst) else default

DEFAULT_OPTIONS = {
    'idml2hubxml_file': False,
    'map': os.getenv("MAP"),
    'empty': getEnvOrDefault("EMPTY"),
    'hierarchy': getEnvOrDefault("HIERARCHY"),
    'cut': getEnvOrDefault("CUT"),
    'names': getEnvOrDefault("NAMES"),
    'typography': getEnvOrDefault("TYPOGRAPHY"),
    'linebreaks': getEnvOrDefault("LINEBREAKS"),
    'prettify': getEnvOrDefault("PRETTIFY"),
    'media': getEnvOrDefault("MEDIA", "Links"),
    'raster': getEnvOrDefault("RASTER", None),
    'vector': getEnvOrDefault("VECTOR", None),
    'idml2hubxml_output': getEnvOrDefault("IDML2HUBXML_OUTPUT_FOLDER", "idml2hubxml"),
    'idml2hubxml_script': os.getenv("IDML2HUBXML_SCRIPT_FOLDER"),
}

LOGGER = logging.basicConfig(filename='idml2docbook.log', encoding='utf-8', level=logging.DEBUG)