from bs4 import BeautifulSoup
import sys
import re
from map import *
from utils import *

def mapList(soup):
    for key, value in MAP.items():
        for el in soup.select(key):
            if "delete" in value and value["delete"]:
                el.decompose()
            elif "unwrap" in value and value["unwrap"]:
                el.unwrap()
            else:
                el.name = value["name"]
                if "classes" in value.keys():
                    el["class"] = value["classes"]
                else:
                    del el["class"]

# We do not need text anchors
# as we will make them ourselves
# and Pandoc doesn't handle it well
def removeTextAnchors(soup):
    for el in soup.select("[id*=\"_idTextAnchor\"]"):
        del el["id"]

def removeOverrideClasses(soup):
    overrideString = "Override-"
    for el in soup.select("[class*=\"" + overrideString + "\"]"):
        newClasses = []
        for c in el["class"]:
            if overrideString not in c:
                newClasses.append(c)
        el['class'] = newClasses

# Pandoc keeps tags with only lang attributes,
# it is for now not something we want to bother with.
def removeLangAttributes(soup):
    for lang in soup.select("[lang]"):
        del lang["lang"]

def handleFootnotes(soup):
    for fn in soup.select("." + FOOTNOTES_CLASS):
        count = 0
        id = ""
        for descendant in fn.descendants:
            if count == 2:  # Stop after removing two
                break
            el = descendant.extract()
            if el.name == "a" :
                id = el["href"].split("#")[-1]
            count += 1
        fn.string = fn.string.strip()
        anchor = soup.find(id=id)
        anchor.string = fn.string
        anchor["class"] = "footnote"
        anchor["id"] = "-".join(anchor["id"].split("-")[:2])
        del anchor["href"]
        anchor.name = "span"
        parent = anchor.parent.parent
        parent.insert_before(anchor)
        parent.decompose()
        fn.decompose()
    for s in soup.select("section._idFootnotes"):
        s.decompose()

# AsciiDoc doesn't allow multilines headers, but the Pandoc AsciiDoc
# writer doesn't seem to care.
# It does remove the linebreaks with the Markdown writer though.
def removeBrFromHeaders(soup):
    for br in soup.select("h1 br, h2 br, h3 br, h4 br, h5 br, h6 br"):
        br.decompose()

def turnIdContainersIntoSections(soup):
    for div in soup.find_all('div', id=lambda x: x and x.startswith('_idContainer')):
        div.name = "section"

def removeSections(soup):
    for s in soup.find_all('section'):
        s.unwrap()

# Adds unnecessary complexity. Adds unnecessary SoftBreaks
# in Pandoc that could not be automatically removed.
def removeEmptyHrefAnchors(soup):
    for a in soup.select('a[href=\"\"]'): a.unwrap()

if __name__ == "__main__":
    # Read the HTML input file
    with open(sys.argv[1], "r") as f:
        html_content = f.read()

    # Use BeautifulSoup to parse and manipulate HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # All the transformations we need to perform...

    # First, take remove the IDs we will for sure not need (see map.py)
    removeIdsToIgnore(soup)

    # Then, clean up the easy mess that was made by InDesign
    removeLangAttributes(soup)
    removeEmptyHrefAnchors(soup)
    soup = removeHyphens(soup, "html.parser")

    # Apply the styles mapping (see map.py)
    mapList(soup)

    # And this part is a bit more contextual... You might want
    # to comment out some of those depending on the context
    # removeOverrideClasses(soup) # Must appear after mapList
    removeTextAnchors(soup) # Must appear after mapList
    handleFootnotes(soup) # Must appear after mapList
    unwrapSuperfluousSpans(soup) # Must appear after mapList
    removeBrFromHeaders(soup) # Must appear after mapList
    turnIdContainersIntoSections(soup)
    removeSections(soup) # Must appear after turnIdContainersIntoSections

    soup = removeEmptyLines(soup, "html.parser")
    # Print the modified HTML to pipe it into Pandoc
    # If you want to read the HTML yourself, you might want to
    # read the output of soup.prettify(). Though, it messes
    # with Pandoc's inlines Elements.
    # To ensure better result, make sure that you print one HTML block
    # per line.
    print(str(soup))
    # print(soup.prettify())
