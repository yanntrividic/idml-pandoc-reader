import sys
import subprocess
from zipfile import ZipFile
from pathlib import Path
from bs4 import BeautifulSoup
import tempfile
import os
from dotenv import load_dotenv

from utils import *
from map import *

load_dotenv()

IDML2XML_FOLDER = os.getenv("IDML2XML_FOLDER")

NODES_TO_REMOVE = [
    "info",
    # "xml-model"
    # "StoryPreference",
    # "InCopyExportOption",
    # "ACE",
    # "Properties",
]

# IDML_TO_DOCBOOK = {
#     "Story": "section"
# }

LAYERS_TO_REMOVE = [
    "Ants"
]

ATTRIBUTES_TO_REMOVE = [
    # "idml2xml:layer", # means that it must be after the previous removals
    # "xmlns:idml2xml",
]

EMPTY_TAGS_TO_REMOVE = [
    "para"
]

def removeUnnecessaryLayers(soup):
    for layer in LAYERS_TO_REMOVE:
        for el in soup.find_all(attrs={"idml2xml:layer": layer}): el.decompose()

def removeUnnecessaryNodes(soup):
    for tag in NODES_TO_REMOVE:
        for el in soup.find_all(tag): el.decompose()

def removeUnnecessaryAttributes(soup):
    for attr in ATTRIBUTES_TO_REMOVE:
        for el in soup.find_all(attrs={attr: True}): del el[attr]

def unwrapUnnecessaryNodes(soup):
    for tag in NODES_TO_UNWRAP:
        for el in soup.find_all(tag): el.unwrap()

def removeEmptyElements(soup):
    for tag in EMPTY_TAGS_TO_REMOVE:
        for el in soup.find_all(tag):
            if el.is_empty_element: el.decompose()
            if not el.text.strip(): el.decompose()

def removeNsAttributes(soup):
    # Remove all css nodes
    for tag in soup.select('css|*'):
        tag.decompose()
    # Remove attributes
    for tag in soup.select("*"):
        toRemove = []
        for attr, _ in tag.attrs.items():
            if attr.startswith("css:") or attr.startswith("xmlns:") or attr.startswith("idml2xml:"):
                toRemove.append(attr)
        for attr in toRemove:
            del tag[attr]

def removeLinebreaks(soup):
    for tag in soup.select("br"):
        tag.string = " "
        tag.unwrap()

def mapList(soup):
    for key, value in MAP.items():
        for el in soup.find_all(attrs={"role": key}):
            if "unwrap" in value and value["unwrap"]:
                el.unwrap()
            if "level" in value and value["type"] == "title":
                el["level"] = value["level"]
            if "type" in value:
                el.name = value["type"]
            if "role" in value:
                el["role"] = value["role"]
            else:
                del el["role"]

def generateXmlId(title_text, xml_ids):
    xml_id = custom_slugify(title_text)
    if xml_id in xml_ids:
        count = sum(xml_id in s for s in xml_ids)
        xml_id = xml_id + "_" + str(count + 1)
    xml_ids.append(xml_id)
    return xml_id

def generateSections(soup):
    """Transform soup to hierarchical sections up to 6 levels deep."""
    new_structure = []
    section_stack = []  # Tracks open sections
    xml_ids = []

    for element in soup.find_all("title"):  # Only processing <title> elements
        try:
            level = int(element.get("level", 1))  # Ensure level is an integer
        except ValueError:
            level = 1  # Default to level 1 if invalid

        title_text = element.get_text(strip=True, separator=" ")
        xml_id = generateXmlId(title_text, xml_ids)

        # Create new section
        section = soup.new_tag("section", **{"xml:id": xml_id})
        title = soup.new_tag("title")
        title.string = title_text
        # print(element.get("role"))
        if "role" in element.attrs:
            # print(element.attrs["role"])
            # print("yes")
            section["role"] = element.attrs["role"]
        section.append(title)

        # Close higher or equal level sections
        while section_stack and section_stack[-1][0] >= level:
            section_stack.pop()

        # Nesting logic
        if section_stack:
            section_stack[-1][1].append(section)  # Add as child of last open section
        else:
            new_structure.append(section)  # Top-level section

        # Push current section to stack
        section_stack.append((level, section))

        # Move following siblings inside the new section
        next_elem = element.find_next_sibling()
        while next_elem and next_elem.name != "title":
            to_move = next_elem
            next_elem = next_elem.find_next_sibling()
            to_move.extract()  # Remove from original place
            section.append(to_move)  # Append to current section

    # Replace soup's body (or a wrapper element) with the new structure
    body = soup.find("article") or soup
    body.clear()
    for sec in new_structure:
        body.append(sec)

    return soup

def idml2xml(file):
    input = IDML2XML_FOLDER + "/" + file
    filename = Path(file).stem
    tmpfile = tempfile.gettempdir()
    # tmpfile = "output"
    cmd = [IDML2XML_FOLDER + "/idml2xml.sh", "-o", tmpfile, file]
    subprocess.run(cmd, capture_output=True) # comment out this line to just get the previous run of idml2xml
    outputfile = tmpfile + "/" + filename + ".xml"
    # print("Output of idml2xml written at: " + outputfile)
    return outputfile

if __name__ == "__main__":
    tmpfile = idml2xml(sys.argv[1])
    # tmpfile = "output/output.xml"

    # Read the HTML input file
    with open(tmpfile, "r") as f:
        xml_content = f.read()

    soup = BeautifulSoup(xml_content, "xml")

    for hub in soup.find_all("hub"):
        hub.name = "article"
        hub["version"] = "5.0"
    for tag in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("xml-model")):
        tag.extract()
    # <article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">

    removeUnnecessaryNodes(soup)
    # removeUnnecessaryLayers(soup)
    removeUnnecessaryAttributes(soup)
    removeEmptyElements(soup)
    soup = removeHyphens(soup, "xml")
    removeNsAttributes(soup)
    mapList(soup)
    generateSections(soup)
    removeLinebreaks(soup)

    # soup.prettify() adds `\n` around inline elements,
    # which is parsed as spaces in Pandoc.
    # str(soup) does it less, but to ensure we don't have
    # this problem, we just remove linebreaks entirely.abs
    result = str(soup).replace("\n", "")
    print(result)

    with open("output/output.xml", "w") as file:
        file.write(soup.prettify())