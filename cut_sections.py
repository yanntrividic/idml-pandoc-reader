import sys
from bs4 import BeautifulSoup
from idml2docbook import idml2docbook
from utils import *

def getCuts():
    """Returns a list of classes that will allow to
    cut the DocBook file in several
    They have a positive "cut" entry in the map."""
    cuts = []
    for key, value in getMap().items():
        if "cut" in value:
            cuts.append(key)
    print(cuts)
    return cuts

def splitDocbook(soup, cuts):
    article_contents = soup.select("article > *")
    # print(article_contents)
    sections = [[]]

    while article_contents:
        if "role" in article_contents[0].attrs:
            print(article_contents[0].attrs["role"])
            if len(sections[-1]) > 0:
                sections.append([])
            sections[-1].append(article_contents.pop(0))
        else: sections[-1].append(article_contents.pop(0))

    return sections

if __name__ == "__main__":
    cuts = getCuts()

    # docbook = idml2docbook(sys.argv[1])

    # For debugging
    with open(sys.argv[1], "r") as f:
        docbook = f.read()

    soup = BeautifulSoup(docbook, "xml")
    print(len(splitDocbook(soup, cuts)))