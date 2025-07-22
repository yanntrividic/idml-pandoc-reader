from bs4 import BeautifulSoup, Tag
import re
import unidecode
import json
import sys

# InDesign leaves hyphens from the INDD file in the HTML export
# Hopefully, it leaves them with a trailing space,
# which allows us to spot them easily with a regular expression.
def remove_hyphens(soup, parser):
    return BeautifulSoup(re.sub(r'([a-zA-ZÀ-Ÿ])\-\s([a-zA-ZÀ-Ÿ])', r'\1\2', str(soup)), parser)

# Pandoc's AST takes into account all spans,
# even if they don't carry any useful information
# this allows to clean the document before sending
# it to Pandoc.
def unwrap_superfluous_spans(soup):
    for s in soup.find_all('span'):
        if not s.attrs:
            s.unwrap()

def remove_empty_lines(soup, parser):
    # There might be a few empty lines laying around:
    return BeautifulSoup(re.sub(r"\n+", r"\n", str(soup)), parser)

def wrap_element_content_in_new_element(soup, el, type, role=None):
    """Takes an element, and wrap its content in a new element.
    is useful to construct valid listitem and blockquote elements."""
    wrapper = soup.new_tag(type)
    if role: wrapper["role"] = role
    wrapper.extend(el.contents)
    el.clear()
    el.append(wrapper)
    return el

def wrap_consecutive_elements(soup, role, wrap_name):
    article = soup.find("article")
    if not article:
        return

    # Only direct children that are Tags
    def is_target(el):
        return isinstance(el, Tag) and el.get("role") == role

    children = [child for child in article.children if isinstance(child, Tag)]
    i = 0

    while i < len(children):
        group = []
        # Only collect consecutive unwrapped targets
        while i < len(children) and is_target(children[i]) and children[i].name != wrap_name:
            group.append(children[i])
            i += 1

        if group:
            insert_index = article.contents.index(group[0])
            wrapper = soup.new_tag(wrap_name)
            wrapper["role"] = role
            for item in group:
                del item["role"]
                wrapper.append(item.extract())
            article.insert(insert_index, wrapper)

            # Refresh children and restart after wrapper
            children = [child for child in article.children if isinstance(child, Tag)]
            i = children.index(wrapper) + 1
        else:
            i += 1

def merge_consecutive_elements(soup, role, type, joiner):
    print(role, type, joiner)
    wrap_consecutive_elements(soup, role, type)
    article = soup.find("article")
    # find all the elements resulting from this wrapping
    for el in article.find_all(type, attrs={"role": role}, recursive=False):
        print(el)
        # for child in el.children:
            # print(child)
            # if isinstance(child, Tag): child.unwrap()