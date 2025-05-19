import sys
from bs4 import BeautifulSoup
from idml2docbook import idml2docbook
from utils import *
import subprocess
import os
from map_helper import *

def get_cuts(file):
    """Returns a list of classes that will allow to
    cut the DocBook file in several
    They have a positive "cut" entry in the map."""
    cuts = []
    for key, value in getMap(file).items():
        if "cut" in value:
            if "role" in value: cuts.append(value[f"role"])
            else: cuts.append(key)
    return cuts

def split_docbook(docbook, **options):
    soup = BeautifulSoup(docbook, "xml")
    cuts = get_cuts(options["map"])
    article_contents = soup.select("article > *")
    # print(article_contents)
    sections = [[]]

    while article_contents:
        if "role" in article_contents[0].attrs and article_contents[0].attrs["role"] in cuts:
            if len(sections[-1]) > 0:
                sections.append([])
            sections[-1].append(str(article_contents.pop(0)))
        else: sections[-1].append(str(article_contents.pop(0)))

    names = []
    for i, _ in enumerate(sections):
        sections[i] = wrap_xml_in_docbook_schema("".join(sections[i]))
        if options["prettify"]: sections[i] = BeautifulSoup(sections[i], "xml").prettify()
        names.append(get_name_from_sections(sections[i]))

    return names, sections


def wrap_xml_in_docbook_schema(xml):
    return ("""<?xml version="1.0" encoding="utf-8"?>""" +
           """<article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">""" +
           xml +
           """</article>""")

def get_name_from_sections(xml):
    soup = BeautifulSoup(xml, "xml")
    sections = soup.select("article > section")
    ids = []
    for section in sections: ids.append(section.attrs["xml:id"])
    return "_".join(ids[:10]).lower()

if __name__ == "__main__":

    docbook = idml2docbook(sys.argv[1])

    # For debugging
    # with open(sys.argv[1], "r") as f:
    #     docbook = f.read()

    soup = BeautifulSoup(docbook, "xml")
    sections = split_docbook(soup, cuts)
    # for section in sections: print(section)

    for i, section in enumerate(sections):
        docbook = wrap_xml_in_docbook_schema("".join(section))
        name = "{:02d}".format(i) + "_" + get_name_from_sections(docbook)
        cmd = [
            os.getenv("PANDOC_EXECUTABLE"),
            "-f", "docbook",
            # "-t", "markdown_phpextra",
            "-t", "native",
            "--lua-filter=lua-filters/roles-to-classes.lua",
            "--lua-filter=lua-filters/collapse-sections-into-headers.lua",
            "--wrap=none",
            "-o", "output/sections/{}.md".format(name)
            # "-o", "output/sections/{}.native".format(name)
        ]

        # with open("output/sections/" + str(i) + ".xml", "w") as file:
        #     file.write(docbook)

        subprocess.run(cmd, input=docbook.encode('utf-8'))