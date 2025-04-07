import sys
from bs4 import BeautifulSoup
from idml2docbook import idml2docbook
from utils import *
import subprocess
import os

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
        if "role" in article_contents[0].attrs and article_contents[0].attrs["role"] in cuts:
            print(article_contents[0].attrs["role"])
            if len(sections[-1]) > 0:
                sections.append([])
            sections[-1].append(str(article_contents.pop(0)))
        else: sections[-1].append(str(article_contents.pop(0)))

    for section in sections: "".join(section)

    return sections


def wrapXmlInDocbookSchema(string):
    return ("""<?xml version="1.0" encoding="utf-8"?>
           <article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">""" +
           string +
           """</article>""")

if __name__ == "__main__":
    cuts = getCuts()

    # docbook = idml2docbook(sys.argv[1])

    # For debugging
    with open(sys.argv[1], "r") as f:
        docbook = f.read()

    soup = BeautifulSoup(docbook, "xml")
    sections = splitDocbook(soup, cuts)
    print(len(sections))
    # for section in sections: print(section)

    for i, section in enumerate(sections):
        cmd = [
            os.getenv("PANDOC_EXECUTABLE"),
            "-f", "docbook",
            "-t", "markdown_phpextra",
            "--lua-filter=roles-to-classes.lua",
            "--wrap=none",
            "-o", "output/sections/{}.md".format(i)
        ]
        docbook = wrapXmlInDocbookSchema("".join(section))

        # with open("output/sections/" + str(i) + ".xml", "w") as file:
        #     file.write(docbook)

        subprocess.run(cmd, input=docbook.encode('utf-8'))