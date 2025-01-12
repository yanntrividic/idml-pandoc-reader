import re
import sys

from map import MAP

def map_to_selector(entry):
    s = ""
    if "name" in entry: s = s + entry.get("name")
    if "classes" in entry: s = s + "." + ".".join(entry.get("classes"))
    if "delete" in entry: return "deleted!"
    if "unwrap" in entry: return "unwrapped!"
    return s

if __name__ == "__main__":
    # Read the HTML input file
    with open(sys.argv[1], "r") as f:
        html_content = f.read()

    tag_and_classes = r'<(\w+)[^>]*\bclass="(.*?)"[^>]*>'

    s = set()
    overrides = set()
    for el in re.findall(tag_and_classes, html_content):
        selector = re.sub(r'\s+', ".", ".".join(el))
        if selector.find("Override") == -1:
            s.add(selector)
        else:
            overrides.add(selector)

    print("Here are all the couples tag/classes present in " + sys.argv[1] + ":")
    print("\n".join(sorted(s)))

    print("\nAnd here are all the overrides (ideally, there would be none):")
    print("\n".join(sorted(overrides)))

    covered = []
    uncovered = []

    for selector in sorted(s):
        if selector in MAP:
            covered.append(selector)
        else:
            uncovered.append(selector)

    print("\n\nHere is the mapping that will be applied:")
    for c in covered:
        print(c + " => " + map_to_selector(MAP.get(c)) )

    print("\n\nAnd here are the elements that won't be handled (overrides excluded):")
    print("\n".join(uncovered))