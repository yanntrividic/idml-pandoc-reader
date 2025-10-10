import re
import sys
import json
import logging
import os
from slugs import custom_slugify
from bs4 import BeautifulSoup
from natsort import natsorted
import natsort as ns
import pandas as pd

BOLD = '\033[1m'
END = '\033[0m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'

BASE_PREFIX_CHARACTER_STYLE = 'override-character-style-'
BASE_PREFIX_PARAGRAPH_STYLE = 'override-paragraph-style-'

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
        for property in ["role", "name"]:
            for el in soup.find_all(attrs={property: value["hub"]}):
                if el[property] != key:
                    el[property] = key
                    if not log:
                        logging.debug("Role name for style \"" + value["native"] + "\" was changed: " + value["hub"] + " -> " + key)
                        log = True

def get_new_role_label(type, number, old_role=None):
    if old_role:
        return f"{old_role}-override-{number}"
    else:
        return f"{type}-override-{number}"

def normalize_attr_name(name: str) -> str:
    """Return the local name with any namespace/prefix removed."""
    if name.startswith('css_namespace__'):
        name = name[len('css_namespace__'):]
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
    relevant_properties = ["remap", "native-name", "role", "name"]
    for k, v in list(tag.attrs.items()):
        # Detect base role (for overrides) and direct formatting

        if looks_like_css_attr(k) or k in relevant_properties : items = filter_property(items, k, v)
    items.sort()
    return tuple(items)

# Some CSS properties are not relevant here, so we might want to
# filter them in order to have more interesting overrides classes...
def filter_property(items, k, v):
    name = normalize_attr_name(k)
    append = True

    # If we ignore this property, pass
    # if name in CSSA_PROPERTIES_TO_IGNORE: append = False
    # # If the color is equivalent to the default color or if is black transparent, pass
    # if v == "device-cmyk(0,0,0,1)": append = False
    # if v == "device-cmyk(0,0,0,0)": append = False
    
    if append: items.append((normalize_attr_name(k), v))

    return items

def turn_direct_formatting_into_custom_roles(xml):
    # Some CSSa (https://github.com/le-tex/CSSa) properties 
    # must be ignored for a smarter overrides detection. 
    # This list needs to be refined
    CSSA_PROPERTIES_TO_IGNORE = [
        "hyphens",                 # usually used for handling rags
        "initial-letter",          # ignoring drop caps
        "letter-spacing",          # usually used for handling rags
        "line-height",             # maybe we can ignore it as well?
        "text-decoration-offset",  # offset with the underlines
        "text-decoration-width",   # width of the underline
    ]

    # Hacky way to enable namespace support for the `css:`-prefixed attributes
    xml = xml.replace('css:', 'css_namespace__')

    soup = BeautifulSoup(xml, "xml")

    paragraph_styles_overrides = {}
    character_styles_overrides = {}

    # Walk only para and phrase
    style_num = 0

    for tag in soup.find_all(['para', 'phrase']):
        # find css-like attrs
        css_items = [(k, v) for k, v in tag.attrs.items() if looks_like_css_attr(k)]
        if not css_items:
            continue

        key = canonical_css_key(tag)

        if tag.name == 'para':
            store = paragraph_styles_overrides
            type = "paragraph"
        else:
            store = character_styles_overrides
            type = "character"

        # --- NEW: per-role stable numbering ---
        old_role = tag.get('role')
        if old_role not in store:
            store[old_role] = {}
        role_store = store[old_role]

        if key not in role_store:
            role_store[key] = len(role_store) + 1

        style_num = role_store[key]
        # --------------------------------------

        # remove the detected css-like attributes from the element
        for k, _ in css_items:
            if k in tag.attrs:
                del tag.attrs[k]

        # update or create role
        new_role = get_new_role_label(type, style_num, old_role if old_role else None)

        tag["role"] = new_role

    return soup, paragraph_styles_overrides, character_styles_overrides
    

def get_styles(xml):
    xml = xml.replace('css:', 'css_namespace__')

    soup = BeautifulSoup(xml, "xml")

    paragraph_styles = {}
    character_styles = {}

    for tag in soup.find_all("css_namespace__rule"):
        
        key = canonical_css_key(tag)

        if tag.attrs["layout-type"] == "para": paragraph_styles[tag.attrs["name"]] = key
        if tag.attrs["layout-type"] == "inline": character_styles[tag.attrs["name"]] = key
    
    return paragraph_styles, character_styles

def save_styles_as_ods(
    paragraph_styles,
    character_styles,
    paragraph_styles_overrides,
    character_styles_overrides,
    filename_stem):

    output_file = f"{filename_stem}.ods"

    pairs = [
        ("paragraph", paragraph_styles, False),
        ("character", character_styles, False),
        ("paragraph", paragraph_styles_overrides, True),
        ("character", character_styles_overrides, True)
    ]

    # TODO: If at some point we want a better looking output
    # https://xlsxwriter.readthedocs.io/working_with_pandas.html
    with pd.ExcelWriter(output_file) as writer:  
        for label, styles, is_override in pairs:
            rows = []

            # Flatten nested structure:
            # styles = { old_role: { key_tuple: num, ... }, ... }
            if is_override:
                for old_role, overrides in styles.items():
                    for k, v in overrides.items():
                        row = {kk: vv for kk, vv in k}  # turn each tuple pair into dict
                        row['base_role'] = old_role  # keep base role
                        # Reconstruct final override name:
                        row['role'] = get_new_role_label(label, v, old_role if old_role else None)
                        rows.append(row)
            else:
                # print(styles)
                for roles, attributes in styles.items():
                    # print(roles, attributes)
                    row = {kk: vv for kk, vv in attributes}  # turn each tuple pair into dict
                    rows.append(row)

            if not rows:
                continue  # skip empty sheets

            df = pd.DataFrame(rows)
            
            # reorder columns
            cols = df.columns.tolist()

            # Ensure 'role', 'base_role', and 'override_num' are first
            ordered = []
            for col in ['name', 'role', 'base_role', 'native-name', 'remap']:
                if col in cols:
                    ordered.append(col)
                    cols.remove(col)
            cols = ordered + natsorted(cols, alg=ns.IGNORECASE)

            df = df[cols]

            df.to_excel(writer, index=False, engine="ods", sheet_name=label + ("_overrides" if is_override else ""))

    print(f"Saved overrides to {output_file}")

def fix_role_names(soup):
    roles = build_roles_map(soup)
    soup = update_roles_with_better_slugs(soup, roles)

def build_dict_from_map_array(map):
    map_dict = {}
    for entry in map:
        map_dict[entry["selector"][1:]] = entry["operation"]
    return map_dict

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input.xml map.json [--to-ods]")
        sys.exit(1)

    to_ods = False

    if "--to-ods" in sys.argv:
        to_ods = True
        sys.argv.remove("--to-ods")

    file = sys.argv[1]
    map_file = sys.argv[2]

    file = sys.argv[1]
    map = get_map(sys.argv[2])
    map = build_dict_from_map_array(map)

    # Read the HTML input file
    with open(file, "r") as f:
        hubxml = f.read()

    # Those three lines fix the roles names
    # If your map file was designed using v0.1.0
    # comment those three lines
    soup = BeautifulSoup(hubxml, "xml")
    fix_role_names(soup)
    hubxml = str(soup)
    if to_ods: paragraph_styles, character_styles = get_styles(hubxml)
    soup, paragraph_styles_overrides, character_styles_overrides = turn_direct_formatting_into_custom_roles(hubxml)
    hubxml = str(soup)

    # Save as ODS
    if to_ods:
        file_stem = os.path.splitext(file)[0]
        save_styles_as_ods(
            paragraph_styles,
            character_styles,
            paragraph_styles_overrides,
            character_styles_overrides,
            file_stem
        )

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
    for couple in natsorted(roles, alg=ns.IGNORECASE):
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
