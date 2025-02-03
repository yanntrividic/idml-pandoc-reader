from bs4 import BeautifulSoup
import re
from map import ID_TO_DELETE

# InDesign leaves hyphens from the INDD file in the HTML export
# Hopefully, it leaves them with a trailing space,
# which allows us to spot them easily with a regular expression.
def removeHyphens(soup, parser):
    return BeautifulSoup(re.sub(r'([a-zA-ZÀ-Ÿ])\-\s([a-zA-ZÀ-Ÿ])', r'\1\2', str(soup)), parser)

# Pandoc's AST takes into account all spans,
# even if they don't carry any useful information
# this allows to clean the document before sending
# it to Pandoc.
def unwrapSuperfluousSpans(soup):
    for s in soup.find_all('span'):
        if not s.attrs:
            s.unwrap()

def removeEmptyLines(soup, parser):
    # There might be a few empty lines laying around:
    return BeautifulSoup(re.sub(r"\n+", r"\n", str(soup)), parser)

def removeIdsToIgnore(soup):
    for id in ID_TO_DELETE:
        el = soup.find(id=id)
        if el: el.decompose()