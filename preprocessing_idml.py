import sys
import subprocess
from zipfile import ZipFile
from pathlib import Path
from bs4 import BeautifulSoup
import tempfile
import os
from dotenv import load_dotenv

from utils import *
from map_idml import *

load_dotenv()

IDML2XML_FOLDER = os.getenv("IDML2XML_FOLDER")

NODES_TO_REMOVE = [
    "info",
    "xml-model"
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

def mapList(soup):
    for key, value in MAP.items():
        for el in soup.find_all(attrs={"role": key}):
            if "level" in value and value["type"] == "title":
                el["level"] = value["level"]
            if "type" in value:
                el.name = value["type"]
            if "role" in value:
                el["role"] = value["role"]
            else:
                del el["role"]

def generateXmlId(title):
    """Generate an XML ID from title text."""
    return re.sub(r'\W+', '_', title.strip()).lower()

def generateSections(soup):
    """Transform soup to hierarchical sections up to 6 levels deep."""
    new_structure = []
    section_stack = []  # Keeps track of open sections by level

    for element in soup.find_all(["title"]):
        level = int(element.get("level", 1))  # Default to level 1 if missing
        title_text = element.get_text(strip=True, separator=" ")  # Preserve line breaks
        xml_id = generateXmlId(title_text)

        # Create new section
        section = soup.new_tag("section", **{"xml:id": xml_id})
        title_tag = soup.new_tag("title")
        title_tag.string = title_text
        section.append(title_tag)

        # Close sections if needed
        while section_stack and section_stack[-1][0] >= level:
            section_stack.pop()

        # Nest the section properly
        if section_stack:
            section_stack[-1][1].append(section)
        else:
            new_structure.append(section)

        # Push to stack
        section_stack.append((level, section))

        # Move following siblings inside this section
        next_elem = element.find_next_sibling()
        while next_elem and next_elem.name != "title":
            to_move = next_elem
            next_elem = next_elem.find_next_sibling()
            to_move.extract()
            section.append(to_move)

    # Replace original content while keeping other elements intact
    for sec in new_structure:
        soup.insert(len(soup.contents), sec)  # Append to body

def idml2xml(file):
    input = IDML2XML_FOLDER + "/" + file
    filename = Path(file).stem
    tmpfile = tempfile.gettempdir()
    # tmpfile = "output"
    cmd = [IDML2XML_FOLDER + "/idml2xml.sh", "-o", tmpfile, file]
    # subprocess.run(cmd) # comment out this line to just get the previous run of idml2xml
    outputfile = tmpfile + "/" + filename + ".xml"
    print("Output of idml2xml written at: " + outputfile)
    return outputfile

if __name__ == "__main__":
    # tmpfile = idml2xml(sys.argv[1])
    tmpfile = "output/Deborder-Bollore_A5_250214.xml"

    # Read the HTML input file
    with open(tmpfile, "r") as f:
        xml_content = f.read()

    soup = BeautifulSoup(xml_content, "xml")

    for hub in soup.find_all("hub"):
        hub.name = "article"
        hub["version"] = "5.0"
    # <article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">

    removeUnnecessaryNodes(soup)
    removeUnnecessaryLayers(soup)
    removeUnnecessaryAttributes(soup)
    removeEmptyElements(soup)
    soup = removeHyphens(soup, "xml")
    removeNsAttributes(soup)
    mapList(soup)
    # generateSections(soup)

    with open("output/output.xml", "w") as file:
        file.write(soup.prettify())

    # Read the HTML input file
    # with ZipFile(sys.argv[1]) as archive:
    #     with archive.open("designmap.xml") as designmap:
    #         designmap_content = designmap.read()
    #     # print(designmap_content)
    #     designmap_soup = BeautifulSoup(designmap_content, "xml")
    #     stories = designmap_soup.Document["StoryList"].split(" ")
    #     stories = [f"Stories/Story_{story}.xml" for story in stories]
    #     stories.pop() # This is the BackingStory we are removing... Should we keep it?
    #     # print(stories)

    #     concatenated_stories = '<?xml version="1.0" encoding="UTF-8"><Stories>'
    #     for story in stories:
    #         with archive.open(story) as storyfile:
    #             story_content = storyfile.read()
    #         story_soup = BeautifulSoup(story_content, "xml")
    #         # print("HELLO ", str(story_soup.Story))
    #         concatenated_stories += str(story_soup.Story)
    #     concatenated_stories += "</Stories>"
    #     # print(concatenated_stories)

    # soup = BeautifulSoup(concatenated_stories, "xml")
    # removeUnnecessaryNodes(soup)
    # unwrapUnnecessaryNodes(soup)
    # print(soup.prettify())
    # s = set()
    # for el in soup.select("CharacterStyleRange"):
    #     s.add(el['AppliedCharacterStyle'])
    # print(s)