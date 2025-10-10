import subprocess
from bs4 import BeautifulSoup, NavigableString
import copy
import os
import re
import logging

from idml2hubxml import *
from utils import *
from slugs import *
from map import *

NODES_TO_REMOVE = [
    "info",
    "sidebar",
    "link"
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
    # "Ants"
]

ATTRIBUTES_TO_REMOVE = [
    # "idml2xml:layer", # means that it must be after the previous removals
    # "xmlns:idml2xml",
]

def remove_unnecessary_layer(soup):
    for layer in LAYERS_TO_REMOVE:
        for el in soup.find_all(attrs={"idml2xml:layer": layer}): el.decompose()

def remove_unnecessary_nodes(soup):
    for tag in NODES_TO_REMOVE:
        for el in soup.find_all(tag): el.decompose()

def remove_unnecessary_attributes(soup):
    for attr in ATTRIBUTES_TO_REMOVE:
        for el in soup.find_all(attrs={attr: True}): del el[attr]

def unwrap_unnecessary_nodes(soup):
    for tag in NODES_TO_UNWRAP:
        for el in soup.find_all(tag):
            logging.debug("Unwrapping " + tag)
            el.unwrap()

def fill_empty_elements_with_br(soup):
    """Adds a <br> tag in every empty para element.
    """
    logging.info("Removing empty elements...")
    for el in soup.find_all("para"):
        if el.is_empty_element:
            el.append(soup.new_tag("br"))

def process_images(soup, wrap_fig = False, rep_raster = None, rep_vector = None, folder = None):
    logging.info("Processing media filenames...")

    for tag in soup.select("para > mediaobject"):
        imagedata = tag.find_next("imagedata")
        fileref = imagedata["fileref"]
        new_fileref = ""

        base, file_ext = os.path.splitext(fileref)
    
        # Decode the base
        base = decode_path(base)

        # Slugify the filename
        filename = base.split("/").pop()
        filename = custom_slugify(filename, 100)
        base = "/".join(base.split("/")[:-1]) + "/" + filename

        if rep_raster and (file_ext.lower() in RASTER_EXTS): new_fileref = base + "." + rep_raster
        elif rep_vector and (file_ext.lower() in VECTOR_EXTS): new_fileref = base + "." + rep_vector
        else: new_fileref = base + file_ext.lower()


        if folder: imagedata["fileref"] = folder + "/" + new_fileref.split("/").pop()
        else: imagedata["fileref"] = new_fileref

        if (rep_raster or rep_vector or folder):
            logging.debug("Media was: " + fileref)
            logging.debug("and is now: " + imagedata["fileref"])

        if(wrap_fig): tag.parent.name = "figure"
        else: tag.parent.unwrap() # no need for a figure!

def remove_ns_attributes(soup):
    # Remove all css nodes
    for tag in soup.select('css|*'):
        tag.decompose()
    # Remove attributes
    for tag in soup.select("*"):
        to_remove = []
        for attr, _ in tag.attrs.items():
            if attr.startswith("css:") or attr.startswith("xmlns:") or attr.startswith("idml2xml:"):
                to_remove.append(attr)
        for attr in to_remove:
            del tag[attr]

def remove_linebreaks(soup):
    """When working with ragged paragraphs, some <br> tags might be added
    It can be handy to replace them with spaces to have more reflowable content."""
    logging.info("Removing linebreaks...")
    for tag in soup.select("br"):
        tag.string = " "
        tag.unwrap()

def replace_linebreaks(string):
    return string.replace("<br/>", "<simpara><?asciidoc-br?></simpara>")

def clean_urls_from_linebreaks(soup):
    """URLs can have line breaks within to compose correct rags.
    This method removes those line breaks by joining the strings that start with http and
    that are separated by a <br/> tag. The URL can't end with a line break in the source file."""
    s = str(soup)

    url_regex_with_br = r"https?:\/\/([-A-zÀ-ÿ0-9]+\.)?([-A-zÀ-ÿ0-9@:%._\+~#=]+(<br/>)?)+\.[A-zÀ-ÿ0-9()]{1,6}(\b[-A-zÀ-ÿ0-9()@:%;_\+.~#?&//=]*(<br/>)?)*"

    def replacer(match):
        return match.group(0).replace(r"<br/>", "")
    
    return BeautifulSoup(re.sub(url_regex_with_br, replacer, s), "xml")

def remove_orthotypography(soup):
    logging.info("Removing input's orthotypography...")
    s = str(soup)

    # Remove non-discretionary hyphens
    non_discretionary_hyphen = u"\u00ad"
    s = s.replace(non_discretionary_hyphen, "")

    # Replace special spaces with spaces
    special_spaces = [
    u"\u00a0", u"\u1680", u"\u180e", u"\u2000", u"\u2001", u"\u2002", u"\u2003", u"\u2004",
    u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", u"\u200a", u"\u200b", u"\u202f",
    u"\u205f", u"\u3000"
    ]

    for space in special_spaces:
        s = s.replace(space, " ")

    return BeautifulSoup(s, "xml")

def move_space_outside_of_phrase(soup, space_chars=" \u00a0\u202f"):
    """
    Move leading/trailing characters from inside <phrase> to outside the tag,
    but IGNORE (do nothing to) <phrase> tags whose content is entirely whitespace.
    """
    for phrase in list(soup.find_all("phrase")):
        if not phrase.string:
            continue

        text = phrase.string  # pure text inside the <phrase>

        # If the phrase is entirely whitespace according to space_chars -> leave it alone
        if text.strip(space_chars) == "":
            continue

        # count leading/trailing whitespace characters (by the defined set)
        leading = len(text) - len(text.lstrip(space_chars))
        trailing = len(text) - len(text.rstrip(space_chars))

        # nothing to do if no leading/trailing spaces
        if not (leading or trailing):
            continue

        # replace inner text with trimmed text
        inner_clean = text.strip(space_chars)
        phrase.string.replace_with(inner_clean)

        if leading:
            logging.debug("Leading space(s) found a <phrase> element, moved before: " + str(phrase))
            lead_spaces = text[:leading]
            prev = phrase.previous_sibling
            if isinstance(prev, NavigableString):
                prev.replace_with(str(prev) + lead_spaces)
            else:
                phrase.insert_before(NavigableString(lead_spaces))

        if trailing:
            logging.debug("Trailing space(s) found a <phrase> element, moved after: " + str(phrase))
            trail_spaces = text[-trailing:]
            nxt = phrase.next_sibling
            if isinstance(nxt, NavigableString):
                nxt.replace_with(trail_spaces + str(nxt))
            else:
                phrase.insert_after(NavigableString(trail_spaces))

    return soup

def add_french_orthotypography(soup, thin_spaces):
    """Applies a series of regex to comply to French orthotypography rules
    if thin_spaces, it only uses non-breaking thin spaces.
    """
    logging.info("Adding new french orthotypography...")

    s = str(soup)

    s = re.sub(r"\s([!\?;€\$%])", u"\u202f" + r'\1', s) # thin spaces
    s = re.sub(r"\s\:", (u"\u202f" if thin_spaces else u"\u00a0") + r':', s) # nbsp, doesn't seem to work...
    s = re.sub(r"(\d)\s(\d\d\d)", r'\1' + u"\u202f" + r'\2', s) # numbers
    s = re.sub(r"«\s?", r'«' + u"\u202f", s) # quotes
    s = re.sub(r"\s?»", u"\u202f" + r'»', s) # quotes
    s = re.sub(r"°\s?", r'°' + u"\u202f", s) # degrees
    s = re.sub(r"\.\.\.", r'…', s) # suspension marks

    return BeautifulSoup(s, "xml")

def hubxml2docbook(file, **options):
    logging.info("hubxml2docbook starting...")
    # Read the HTML input file
    with open(file, "r") as f:
        xml_content = f.read()

    logging.info(file + " read succesfully!")

    soup = BeautifulSoup(xml_content, "xml")

    # This line fixes the roles names
    # If your map file was designed using v0.1.0, comment it
    fix_role_names(soup)

    for hub in soup.find_all("hub"):
        hub.name = "article"
        hub["version"] = "5.0"
    for tag in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("xml-model")):
        tag.extract()
    # <article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">

    if not options["ignore_overrides"]: soup, _, _ = turn_direct_formatting_into_custom_roles(str(soup))

    remove_unnecessary_nodes(soup)
    # remove_unnecessary_layer(soup)
    remove_unnecessary_attributes(soup)
    remove_ns_attributes(soup)

    process_images(soup,
        False,
        options["raster"],
        options["vector"],
        options["media"])

    soup = clean_urls_from_linebreaks(soup) # must be done before remove_linebreaks and removeHyphens

    if not options["linebreaks"]: remove_linebreaks(soup)

    fill_empty_elements_with_br(soup)

    soup = remove_hyphens(soup, "xml")

    if options["typography"]:
        soup = remove_orthotypography(soup)
        soup = move_space_outside_of_phrase(soup)
        soup = add_french_orthotypography(soup, options["thin_spaces"])

    if options["prettify"]:
        logging.warning("Prettifying can result in errors depending on whatcha wanna do afterwards!")
        docbook = soup.prettify()
        # prettify adds `\n` around inline elements,
        # which is parsed as spaces in Pandoc.
        # str(soup) does it less, but to ensure we don't have
        # this problem, we just remove linebreaks entirely.
    else:
        docbook = str(soup).replace("\n", "")

    docbook = replace_linebreaks(docbook)

    logging.info("hubxml2docbook done.")

    return docbook

def idml2docbook(input, **options):
    logging.info("idml2docbook starting...")
    if options["idml2hubxml_file"]:
        hubxml = input
        logging.warning("Directly reading the input as a hubxml file.")
    else:
        hubxml = idml2hubxml(input, **options)
    docbook = hubxml2docbook(hubxml, **options)
    logging.info("idml2docbook done.")
    return docbook