import re
import sys
import json
import logging
from slugs import custom_slugify
from bs4 import BeautifulSoup
from natsort import natsorted

BOLD = '\033[1m'
END = '\033[0m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'

def get_map(file):
    logging.info("Reading map file at: " + file)
    f = open(file)
    # returns JSON object as a list 
    data = None
    try:
        data = json.load(f)
        logging.debug("Data read from map file: " + str(data))
    except:
        logging.warning("No data was read from map file.")
    return data

def log_map_entry(entry):
    s = ""
    if "type" in entry: s = s + entry.get("type")
    if "classes" in entry: s = s + ("." + entry.get("classes") if entry.get("classes") else "" )
    if "level" in entry: s = s + " [level " + str(entry.get("level")) + "]"
    if "simplify" in entry: s = s + "[simplified!]"
    if "empty" in entry: s = s + "[empty kept]"
    if "br" in entry: s = s + "[linebreak inserted]"
    if "wrap" in entry: s = s + "[in " + str(entry.get("wrap")) + "]"
    if "attrs" in entry: s = s + "[attrs added " + str(entry.get("attrs")) + "]"
    if "delete" in entry: return "deleted!"
    if "unwrap" in entry: return "unwrapped!"
    if s == "": return "no operation applied!"
    return s

def bold_print(s):
    print(BOLD + s + END)

def build_roles_map(soup):
    """Takes a Hub XML soup as input, and builds a dict
    containing the exact InDesign style, the Hub role name,
    if the style is a default one, and a slugified role name as key."""
    roles = {}
    for rule in soup.find_all("css:rule"):
        if "native-name" in rule.attrs:
            to_slugify = native = rule.attrs["native-name"]
            default = False
            
            if native.startswith("$ID/"):
                default = True
                to_slugify = native[4:]
            slug = custom_slugify(to_slugify)

            roles[slug] = {"hub": rule.attrs["name"], "native": native, "default": default}
    return roles

def update_roles_with_better_slugs(soup, roles):
    """Takes a Hub XML soup and the corresponding roles
    map, and updates the roles."""
    for key, value in roles.items():
        log = False
        for el in soup.find_all(attrs={"role": value["hub"]}):
            if el["role"] != key:
                el["role"] = key
                if not log:
                    logging.debug("Role name for style \"" + value["native"] + "\" was changed: " + value["hub"] + " -> " + key)
                    log = True

def turn_direct_formatting_into_custom_roles(xml):
    # Hacky way to enable namespace support for the `css:`-prefixed attributes
    xml = xml.replace('css:', 'css_namespace__')

    soup = BeautifulSoup(xml, "xml")

    paragraph_styles = {}
    character_styles = {}

    def normalize_attr_name(name: str) -> str:
        """Return the local name with any namespace/prefix removed."""
        if name.startswith('css_namespace__'):
            name = name[len('css_namespace__'):]
        # remove any 'prefix:' (css:font-size -> font-size)
        if ':' in name:
            name = name.split(':', 1)[1]
        return name

    def looks_like_css_attr(name: str):
        """
        Heuristic: detect attributes that were intended as css:*,
        which means attributes that start with the css_namespace__ prefix
        """
        if name.startswith('css_namespace__'):
            return True
        return False

    def canonical_css_key(tag):
        """Create a stable tuple key of (localname, value) sorted by name/value."""
        items = []
        for k, v in list(tag.attrs.items()):
            if looks_like_css_attr(k):
                items.append((normalize_attr_name(k), v))
        items.sort()
        return tuple(items)

    # Walk only para and phrase
    for tag in soup.find_all(['para', 'phrase']):
        # find css-like attrs
        css_items = [(k, v) for k, v in tag.attrs.items() if looks_like_css_attr(k)]
        if not css_items:
            continue

        key = canonical_css_key(tag)

        if tag.name == 'para':
            store = paragraph_styles
            base_prefix = 'override-paragraph-style-'
        else:
            store = character_styles
            base_prefix = 'override-character-style-'

        if key not in store:
            store[key] = len(store) + 1
        style_num = store[key]

        # remove the detected css-like attributes from the element
        for k, _ in css_items:
            if k in tag.attrs:
                del tag.attrs[k]

        # update or create role
        old_role = tag.get('role')
        if old_role:
            tag['role'] = f"{old_role}-override-{style_num}"
        else:
            tag['role'] = f"{base_prefix}{style_num}"

    return soup

def fix_role_names(soup):
    roles = build_roles_map(soup)
    soup = update_roles_with_better_slugs(soup, roles)

def build_dict_from_map_array(map):
    map_dict = {}
    for entry in map:
        map_dict[entry["selector"][1:]] = entry["operation"]
    return map_dict

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file = sys.argv[1]
        map = get_map(sys.argv[2])
        map = build_dict_from_map_array(map)

        # Read the HTML input file
        with open(file, "r") as f:
            hubxml = f.read()

        # Those three lines fix the roles names
        # If your map file was designed using v0.1.0
        # comment those three lines
        soup = turn_direct_formatting_into_custom_roles(hubxml)
        fix_role_names(soup)
        hubxml = str(soup)

        type_and_role = r'<(\w+)[^>]*\brole="(.*?)"[^>]*>'

        roles = set()
        covered = []
        uncovered = []

        # We are only interested in what is after the info tag
        try:
            for el in re.findall(type_and_role, hubxml.split("</info>")[1]):
                if not el[1].startswith("hub"): roles.add((el[1], el[0]))
                # And not interested in hub specific tags
        except:
            raise ValueError("This file doesn't seem to be coming from idml2xml...")

        bold_print("Role/tag couples present in " + file + ":")
        for couple in natsorted(roles):
            print("- " + couple[0] + " (" + couple[1] + ")")
            if map and couple[0] not in map:
                uncovered.append(couple)
            else:
                covered.append(couple[0])

        if map:
            print(OKGREEN)
            if len(covered) > 0 :
                bold_print("Applied mapping:")
                for c in covered:
                    print("- " + c + " => " + log_map_entry(map[c]))
            else:
                bold_print(WARNING + (sys.argv[2] if (len(sys.argv) == 3) else DEFAULT_MAP) + " does not apply to " + file)

            if len(uncovered) > 0 :
                print(WARNING)
                bold_print("Unhandled elements:")
                for c in uncovered:
                    print("- " + c[0] + " (" + c[1] + ")")
            else:
                print(OKGREEN + "All elements are covered!")
            print(END)
        else:
            print("\nNo data was read from the map file!")
    else:
        print("This script takes to arguments:")
        print("1) an output XML file from Transpect's idml2xml")
        print("2) a JSON map file designed for idml2docbook")