from bs4 import BeautifulSoup
import re
import unidecode

# InDesign leaves hyphens from the INDD file in the HTML export
# Hopefully, it leaves them with a trailing space,
# which allows us to spot them easily with a regular expression.
def removeHyphens(soup, parser):
    return BeautifulSoup(re.sub(r'([a-zA-ZÀ-Ÿ])\-\s([a-zA-ZÀ-Ÿ])', r'\1\2', str(soup)), parser)

# Pandoc's AST takes into account all spans,
# even if they don't carry any useful information
# this allows to clean the document before sending
# it to Pandoc.
def unwrapSuperfluousSpans(soup):
    for s in soup.find_all('span'):
        if not s.attrs:
            s.unwrap()

def removeEmptyLines(soup, parser):
    # There might be a few empty lines laying around:
    return BeautifulSoup(re.sub(r"\n+", r"\n", str(soup)), parser)

# And we also need a custom filter to generate
# the file-like titles in the left sidebar
def custom_slugify(string):
    regex_subs = [
        (r"[’°:;,]", " "), # replaces punctuation with spaces
        (r"[^\w\s-]", ""),  # remove non-alphabetical/whitespace/'-' chars
        (r"(?u)\A\s*", ""),  # strip leading whitespace
        (r"(?u)\s*\Z", ""),  # strip trailing whitespace
        (r"[-\s_]+", "_"),  # reduce multiple whitespace or '-' to single '_'
    ]
    full_slug = slugify(string, regex_subs, preserve_case=True, use_unicode=True)
    return "_".join(full_slug.split("_")[:5])

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