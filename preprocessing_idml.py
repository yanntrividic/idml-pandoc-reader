import sys
import subprocess
from zipfile import ZipFile
from pathlib import Path
from bs4 import BeautifulSoup
import tempfile
import os
from dotenv import load_dotenv

from utils import *

load_dotenv()

IDML2XML_FOLDER = os.getenv("IDML2XML_FOLDER")

# NODES_TO_REMOVE = [
#     "StoryPreference",
#     "InCopyExportOption",
#     "ACE",
#     "Properties",
# ]

# NODES_TO_UNWRAP = [
#     "idPkg:Story"
# ]

# IDML_TO_DOCBOOK = {
#     "Story": "section"
# }

def removeUnnecessaryNodes(soup):
    for tag in NODES_TO_REMOVE:
        for el in soup.find_all(tag): el.decompose()

def unwrapUnnecessaryNodes(soup):
    for tag in NODES_TO_UNWRAP:
        for el in soup.find_all(tag): el.unwrap()

def removeCss(soup):
    # Remove all css nodes
    for tag in soup.select('css|*'):
        tag.decompose()
    # Remove attributes
    for tag in soup.select("para,phrase"):
        toRemove = []
        for attr, _ in tag.attrs.items():
            if attr.startswith("css:"):
                toRemove.append(attr)
        for attr in toRemove:
            del tag[attr]
        

def idml2xml(file):
    input = IDML2XML_FOLDER + "/" + file
    filename = Path(file).stem
    # tmpfile = tempfile.gettempdir()
    tmpfile = "output"
    cmd = [IDML2XML_FOLDER + "/idml2xml.sh", "-o", tmpfile, file]
    # subprocess.run(cmd)
    return tmpfile + "/" + filename + ".xml"

if __name__ == "__main__":
    tmpfile = idml2xml(sys.argv[1])

    # Read the HTML input file
    with open(tmpfile, "r") as f:
        xml_content = f.read()

    soup = BeautifulSoup(xml_content, "xml")
    soup = removeHyphens(soup, "xml")
    removeCss(soup)
    print(soup.prettify())

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