import re
import sys
import json
import logging
from slugs import custom_slugify
from bs4 import BeautifulSoup

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
        data = json.load(f)[0]
        logging.debug("Data read from map file: " + str(data))
    except:
        logging.warning("No data was read from map file.")
    return data

def log_map_entry(entry):
    s = ""
    if "type" in entry: s = s + entry.get("type")
    if "role" in entry: s = s + "." + entry.get("role").replace(" ", ".")
    if "level" in entry: s = s + " (level " + str(entry.get("level")) + ")"
    if "delete" in entry: return "deleted!"
    if "unwrap" in entry: return "unwrapped!"
    return s

def bold_print(s):
    print(BOLD + s + END)

def build_roles_map(soup):
    """Takes a Hub XML soup as input, and builds a dict
    containing the exact InDesign style, the Hub role name,
    if the style is a default one, and a slugified role name as key."""
    roles = {}
    for rule in soup.find_all("css:rule"):
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

def fix_role_names(soup):
    roles = build_roles_map(soup)
    soup = update_roles_with_better_slugs(soup, roles)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file = sys.argv[1]
        map = get_map(sys.argv[2])

        # Read the HTML input file
        with open(file, "r") as f:
            hubxml = f.read()

        # Those three lines fix the roles names
        # If your map file was designed using v0.1.0
        # comment those three lines
        soup = BeautifulSoup(hubxml, "xml")
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
        for couple in sorted(roles):
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