from bs4 import BeautifulSoup, Tag
import re
import unidecode
import json
import sys

# InDesign leaves hyphens from the INDD file in the HTML export
# Hopefully, it leaves them with a trailing space,
# which allows us to spot them easily with a regular expression.
def remove_hyphens(soup, parser):
    return BeautifulSoup(re.sub(r'([a-zA-ZÀ-Ÿ])\-\s([a-zA-ZÀ-Ÿ])', r'\1\2', str(soup)), parser)

# Pandoc's AST takes into account all spans,
# even if they don't carry any useful information
# this allows to clean the document before sending
# it to Pandoc.
def unwrap_superfluous_spans(soup):
    for s in soup.find_all('span'):
        if not s.attrs:
            s.unwrap()

def remove_empty_lines(soup, parser):
    # There might be a few empty lines laying around:
    return BeautifulSoup(re.sub(r"\n+", r"\n", str(soup)), parser)