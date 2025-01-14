from zipfile import ZipFile
import sys
from bs4 import BeautifulSoup


NODES_TO_REMOVE = [
    "StoryPreference",
    "InCopyExportOption",
    "ACE",
    # "Properties",
]

NODES_TO_UNWRAP = [
    "idPkg:Story"
]

def removeUnnecessaryNodes(soup):
    for tag in NODES_TO_REMOVE:
        for el in soup.find_all(tag): el.decompose()

def unwrapUnnecessaryNodes(soup):
    for tag in NODES_TO_UNWRAP:
        for el in soup.find_all(tag): el.unwrap()

if __name__ == "__main__":
    # Read the HTML input file
    with ZipFile(sys.argv[1]) as archive:
        with archive.open("designmap.xml") as designmap:
            designmap_content = designmap.read()
        # print(designmap_content)
        designmap_soup = BeautifulSoup(designmap_content, "xml")
        stories = designmap_soup.Document["StoryList"].split(" ")
        stories = [f"Stories/Story_{story}.xml" for story in stories]
        stories.pop() # This is the BackingStory we are removing... Should we keep it?
        # print(stories)

        concatenated_stories = '<?xml version="1.0" encoding="UTF-8"><Stories>'
        for story in stories:
            with archive.open(story) as storyfile:
                story_content = storyfile.read()
            story_soup = BeautifulSoup(story_content, "xml")
            # print("HELLO ", str(story_soup.Story))
            concatenated_stories += str(story_soup.Story)
        concatenated_stories += "</Stories>"
        # print(concatenated_stories)

    soup = BeautifulSoup(concatenated_stories, "xml")
    removeUnnecessaryNodes(soup)
    unwrapUnnecessaryNodes(soup)
    print(soup.prettify())
    # s = set()
    # for el in soup.select("CharacterStyleRange"):
    #     s.add(el['AppliedCharacterStyle'])
    # print(s)