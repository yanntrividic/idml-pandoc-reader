import urllib
import os
import sys
import re

RASTER_EXTS = [".tif", ".tiff", ".png", ".jpg", ".jpeg", ".psd"]
VECTOR_EXTS = [".svg", ".eps", ".ai", ".pdf"]

# And we also need a custom filter to generate
# the file-like titles in the left sidebar
def custom_slugify(string, length=5):
    regex_subs = [
        (r"[’°:;,\(\)\*]", " "), # replaces punctuation with spaces
        (r"[^\w\s-]", ""),  # remove non-alphabetical/whitespace/'-' chars
        (r"(?u)\A\s*", ""),  # strip leading whitespace
        (r"(?u)\s*\Z", ""),  # strip trailing whitespace
        (r"[-\s_]+", "_"),  # reduce multiple whitespace or '-' to single '_'
    ]
    full_slug = slugify(string, regex_subs, preserve_case=True, use_unicode=True)
    return "_".join(full_slug.split("_")[:length])

def slugify(value, regex_subs=(), preserve_case=False, use_unicode=False):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Took from Pelican sources.

    For a set of sensible default regex substitutions to pass to regex_subs
    look into pelican.settings.DEFAULT_CONFIG['SLUG_REGEX_SUBSTITUTIONS'].
    """

    import unicodedata
    import unidecode

    def normalize_unicode(text):
        # normalize text by compatibility composition
        # see: https://en.wikipedia.org/wiki/Unicode_equivalence
        return unicodedata.normalize("NFD", text)

    # normalization
    value = normalize_unicode(value)

    if not use_unicode:
        # ASCII-fy
        value = unidecode.unidecode(value)

    # perform regex substitutions
    for src, dst in regex_subs:
        value = re.sub(
            normalize_unicode(src), normalize_unicode(dst), value, flags=re.IGNORECASE
        )

    if not preserve_case:
        value = value.lower()

    return value.strip()

def decode_path(encoded_path):
    """In IDML, paths are encoded as URLs.
    It is sometimes necessary to decode them."""
    return urllib.parse.unquote(encoded_path)

def generate_xml_id(title_text, xml_ids):
    xml_id = custom_slugify(title_text)
    if xml_id in xml_ids:
        count = sum(xml_id in s for s in xml_ids)
        xml_id = xml_id + "_" + str(count + 1)
    xml_ids.append(xml_id)
    return xml_id

def main(folder):
    # Define allowed extensions
    ALLOWED_EXTENSIONS = RASTER_EXTS + VECTOR_EXTS
    
    folder = os.path.abspath(folder)

    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        return

    print(f"Scanning directory: {folder}\n")

    files_to_rename = []

    for filename in os.listdir(folder):
        full_path = os.path.join(folder, filename)
        if os.path.isfile(full_path):
            base, ext = os.path.splitext(filename)
            if ext.lower() in ALLOWED_EXTENSIONS:
                new_base = custom_slugify(base, 100)
                if new_base != base:
                    new_filename = new_base + ext
                    files_to_rename.append((filename, new_filename))

    if not files_to_rename:
        print("No files to rename.")
        return

    print("Proposed renames:\n")
    for old, new in files_to_rename:
        print(f"{old} -> {new}")

    confirm = input("\nDo you want to proceed with these renames? (y/n): ").strip().lower()
    if confirm == 'y':
        for old, new in files_to_rename:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {old} -> {new}")
            else:
                print(f"Skipped (target exists): {old} -> {new}")
    else:
        print("Renaming aborted.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python slugs.py <relative-folder-path>")
    else:
        main(sys.argv[1])