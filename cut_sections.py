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
    return cuts

def splitDocbook(soup, cuts):
    article_contents = soup.select("article > *")
    # print(article_contents)
    sections = [[]]

    while article_contents:
        if "role" in article_contents[0].attrs and article_contents[0].attrs["role"] in cuts:
            if len(sections[-1]) > 0:
                sections.append([])
            sections[-1].append(str(article_contents.pop(0)))
        else: sections[-1].append(str(article_contents.pop(0)))

    for section in sections: "".join(section)

    return sections


def wrapXmlInDocbookSchema(xml):
    return ("""<?xml version="1.0" encoding="utf-8"?>
           <article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">""" +
           xml +
           """</article>""")

def getNameFromSections(xml):
    soup = BeautifulSoup(xml, "xml")
    sections = soup.select("article > section")
    ids = []
    for section in sections: ids.append(section.attrs["xml:id"])
    return "_".join(ids).lower()

if __name__ == "__main__":
    cuts = getCuts()

    # docbook = idml2docbook(sys.argv[1])

    # For debugging
    with open(sys.argv[1], "r") as f:
        docbook = f.read()

    soup = BeautifulSoup(docbook, "xml")
    sections = splitDocbook(soup, cuts)
    # for section in sections: print(section)

    for i, section in enumerate(sections):
        docbook = wrapXmlInDocbookSchema("".join(section))
        name = "{:02d}".format(i) + "_" + getNameFromSections(docbook)
        cmd = [
            os.getenv("PANDOC_EXECUTABLE"),
            "-f", "docbook",
            "-t", "markdown_phpextra",
            "--lua-filter=roles-to-classes.lua",
            "--lua-filter=collapse-sections-into-headers.lua",
            "--wrap=none",
            "-o", "output/sections/{}.md".format(name)
        ]

        # with open("output/sections/" + str(i) + ".xml", "w") as file:
        #     file.write(docbook)

        subprocess.run(cmd, input=docbook.encode('utf-8'))