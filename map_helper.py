import re
import sys
import json

DEFAULT_MAP = "map.json"

BOLD = '\033[1m'
END = '\033[0m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'

def getMap():
    map = DEFAULT_MAP
    if len(sys.argv) == 3:
        map = sys.argv[2]
    # Opening JSON file 
    f = open(map)
    # returns JSON object as a list 
    data = json.load(f)[0]
    return data

def log_map_entry(entry):
    s = ""
    if "type" in entry: s = s + entry.get("type")
    if "role" in entry: s = s + "." + entry.get("role")
    if "level" in entry: s = s + " (level " + str(entry.get("level")) + ")"
    if "delete" in entry: return "deleted!"
    if "unwrap" in entry: return "unwrapped!"
    return s

def boldprint(s):
    print(BOLD + s + END)

if __name__ == "__main__":
    map = getMap()
    file = sys.argv[1]

    # Read the HTML input file
    with open(file, "r") as f:
        docbook = f.read()

    type_and_role = r'<(\w+)[^>]*\brole="(.*?)"[^>]*>'

    roles = set()
    covered = []
    uncovered = []

    for el in re.findall(type_and_role, docbook):
        roles.add((el[1], el[0]))

    boldprint("Role/tag couples present in " + file + ":")
    for couple in sorted(roles):
        print("- " + couple[0] + " (" + couple[1] + ")")
        if couple[0] in map:
            covered.append(couple[0])
        else:
            uncovered.append(couple)

    print(OKGREEN)
    if len(covered) > 0 :
        boldprint("Applied mapping:")
        for c in covered:
            print("- " + c + " => " + log_map_entry(map[c]))
    else:
        boldprint(WARNING + (sys.argv[2] if (len(sys.argv) == 3) else DEFAULT_MAP) + " does not apply to " + file)

    if len(uncovered) > 0 :
        print(WARNING)
        boldprint("Unhandled elements:")
        for c in uncovered:
            print("- " + c[0] + " (" + c[1] + ")")
    else:
        print(OKGREEN + "All elements are covered!")
    print(END)