import sys

from idml2docbook import idml2docbook

def main(argv=None, stdout=None, stdin=None):
    docbook = idml2docbook(sys.argv[1])
    print(docbook)

if __name__ == "__main__":
    main()