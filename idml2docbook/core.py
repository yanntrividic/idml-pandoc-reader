import subprocess
from bs4 import BeautifulSoup
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
    "Ants"
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

def remove_empty_elements(soup, map):
    """Removes empty paras, except when the para has a "empty" entry
    in the map. Must be called before map_list so that it is applied on all elements.
    """
    logging.info("Removing empty elements...")
    for el in soup.find_all("para"):
        if el.is_empty_element:
            if "role" in el.attrs:
                role = el.attrs["role"]
                if role in map and "empty" not in map[role]:
                    el.decompose()
                else:
                    logging.warning("Empty \"" + role + "\" has been kept.")

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

def process_listitems(soup, map):
    logging.info("Wrapping listitem...")
    for el in soup.find_all("listitem"):
        el = wrap_element_content_in_new_element(soup, el, "para")

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

def map_list(soup, map):
    """Takes a soup and a map as arguments.
    Performs a series of operations depending
    on what the map describes.
    """
    logging.info("Starting to apply the styles' mapping...")
    for key, value in map.items():
        for el in soup.find_all(attrs={"role": key}):
            if "unwrap" in value and value["unwrap"]:
                el.unwrap()
            if "delete" in value and value["delete"]:
                el.decompose()
            if "br" in value and value["br"]:
                el.insert_before(soup.new_tag("br"))
            if "level" in value and value["type"] == "title":
                el["level"] = value["level"]
            if "type" in value:
                el.name = value["type"]
            # If the map's "wrap" entry is on, wraps all consecutive
            # elements with the same role in a "wrap" element wrapper.
            # Their role is passed to the wrapper element.
            if "wrap" in value and value["wrap"]:
                wrap_consecutive_elements(soup, key, value["wrap"])

def apply_new_roles(soup, map):
    """Apply new roles after every other operation is done.
    It removes the roles on empty entries, removes it when role="",
    or changes it to the new proposed value.
    It must be done in the end to keep the original paragraph and
    character styles from the IDML document in the rest of the
    computation process"""
    logging.info("Starting to cleaning the roles...")
    for key, value in map.items():
        for el in soup.find_all(attrs={"role": key}):
            if "role" in value:
                el["role"] = value["role"]
                if el["role"] == "": del el["role"]
            if not value: # when the dict is empty, remove the role
                if el.has_attr("role"):
                    del el["role"]

def wrap_consecutive_elements_from_map(soup, map):
    """If the map's "wrap" entry is on, wraps all consecutive
    elements with the same role in a "wrap" element wrapper.
    Their role is passed to the wrapper element."""
    logging.info("Starting to wrap elements with specific roles...")
    for key, value in map.items():
        if "wrap" in value and value["wrap"]:
            wrap_consecutive_elements(soup, key, value["wrap"])

def merge_consecutive_elements_from_map(soup, map):
    """If the map's "merge" entry is on, merges all consecutive elements
    elements with the same role.
    The value in the "merge" specifies a joiner."""
    logging.info("Starting to wrap elements with specific roles...")
    for key, value in map.items():
        if "merge" in value and value["merge"] and "type" in value and "role" in value:
            merge_consecutive_elements(soup, value["role"], value["type"], value["merge"])

def generate_sections(soup):
    """Transform soup to hierarchical sections up to 6 levels deep."""
    logging.info("Generating nested sections' hierarchy...")

    new_structure = []
    section_stack = []  # Tracks open sections
    xml_ids = []
    first_elements = []

    # All the elements, after a title tag are processed by the rest of the method
    # this loop is to preserve what comes before the fisrt title tag
    article_contents = soup.select("article > *")
    while len(article_contents) > 0 and article_contents[0].name != "title":
        first_elements.append(article_contents.pop(0))

    for element in soup.find_all("title"):  # Only processing <title> elements
        try:
            level = int(element.get("level", 1))  # Ensure level is an integer
        except ValueError:
            level = 1  # Default to level 1 if invalid

        title_text = element.get_text(strip=True, separator=" ")
        xml_id = generate_xml_id(title_text, xml_ids)

        # Create new section
        section = soup.new_tag("section", **{"xml:id": xml_id})
        new_title = copy.copy(element) # clone the element to keep it as is.
        if "role" in new_title.attrs: section["role"] = new_title.attrs["role"]
        section.append(new_title)

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

    # Replace soup's article (or a wrapper element) with the new structure
    article = soup.find("article") or soup
    article.clear()

    for elem in first_elements:
        article.append(elem)
    for sec in new_structure:
        article.append(sec)

    return soup

def hubxml2docbook(file, **options):
    logging.info("hubxml2docbook starting...")
    # Read the HTML input file
    with open(file, "r") as f:
        xml_content = f.read()

    map = {}
    if options["map"]:
        map = get_map(options["map"])
    else:
        logging.warning("No map was specified. The conversion might not result in what you want.")

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

    remove_unnecessary_nodes(soup)
    # remove_unnecessary_layer(soup)
    remove_unnecessary_attributes(soup)
    remove_ns_attributes(soup)

    if not options["empty"]:
        remove_empty_elements(soup, map)
    else:
        logging.warning("Keeping empty elements with roles... It might keep unwanted residuous elements!")

    process_images(soup,
        False,
        options["raster"],
        options["vector"],
        options["media"])

    soup = clean_urls_from_linebreaks(soup) # must be done before remove_linebreaks and removeHyphens

    if not options["linebreaks"]: remove_linebreaks(soup) # must be done before mapèlist

    soup = remove_hyphens(soup, "xml")

    if options["typography"]:
        soup = remove_orthotypography(soup)
        soup = add_french_orthotypography(soup, options["thin_spaces"])

    if options["map"]: map_list(soup, map)

    process_listitems(soup, map)
    # join_elements(soup)

    apply_new_roles(soup, map)

    # merge_consecutive_elements_from_map(soup, map)

    if not options["hierarchy"]: generate_sections(soup)


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