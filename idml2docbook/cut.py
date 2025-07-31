import sys
from bs4 import BeautifulSoup
from core import idml2docbook
from utils import *
import subprocess
import os
from map import *

def get_cuts(file):
    """Returns a list of classes that will allow to
    cut the DocBook file in several
    They have a positive "cut" entry in the map."""
    logging.info("Retrieving cuts from: " + file)
    cuts = []
    for key, value in get_map(file).items():
        if "cut" in value:
            if "role" in value: cuts.append(value[f"role"])
            else: cuts.append(key)
    logging.info("Cuts are: " + str(cuts))
    return cuts

def split_docbook(docbook, **options):
    logging.info("Splitting DocBook file...")
    soup = BeautifulSoup(docbook, "xml")
    cuts = get_cuts(options["map"])
    article_contents = soup.select("article > *")
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

    logging.info("Found " + str(len(sections)) + " sections!")
    return names, sections


def wrap_xml_in_docbook_schema(xml):
    return ("""<?xml version="1.0" encoding="utf-8"?>""" +
           """<article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">""" +
           xml +
           """</article>""")

def get_name_from_sections(xml):
    """Turning level 1 sections ids into a filename"""
    soup = BeautifulSoup(xml, "xml")
    sections = soup.select("article > section")
    ids = []
    for section in sections: ids.append(section.attrs["xml:id"])
    return "_".join(ids[:10]).lower()