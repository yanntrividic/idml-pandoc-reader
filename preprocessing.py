from bs4 import BeautifulSoup
import sys
import re
from map import MAP

# Read the HTML input file
with open(sys.argv[1], "r") as f:
    html_content = f.read()

# Use BeautifulSoup to parse and manipulate HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find all divs where the id starts with '_idContainer'
for div in soup.find_all('div', id=lambda x: x and x.startswith('_idContainer')):
    # Replace the div with its children by unwrapping the div
    div.unwrap()  # This removes the div and keeps the children in place
    # div.name = "section"

def mapList(soup):
    for key, value in MAP.items():
        for el in soup.select(key):
            el.name = value["name"]
            if "classes" in value.keys():
                el["class"] = value["classes"]
            else:
                del el["class"]

mapList(soup)

def removeHyphens(soup):
    return BeautifulSoup(re.sub(r'([a-zA-ZÀ-Ÿ])\-\s([a-zA-ZÀ-Ÿ])', r'\1\2', str(soup)), "html.parser")

soup = removeHyphens(soup)

def handleFootnotes(soup):
    # for fn in soup.select(".Note_de_bas_de_pages"):
    #     for child in fn.descendants:
    #         print(child)
    for fn in soup.select(".Note_de_bas_de_pages"):
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

handleFootnotes(soup)

# Print the modified HTML
print(soup.prettify())