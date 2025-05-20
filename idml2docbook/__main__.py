"""Command-line interface to idml2docbook."""

import argparse
import logging
import os

from . import __version__, DEFAULT_OPTIONS, LOGGER
from .idml2docbook import idml2docbook
from .cut import split_docbook

# This file structure is inspired from weasyprint:
# https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/__main__.py
class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        self._arguments = {}
        super().__init__(*args, **kwargs)

    # def add_argument(self, *args, **kwargs):
    #     super().add_argument(*args, **kwargs)
    #     key = args[-1].lstrip('-')
    #     kwargs['flags'] = args
    #     kwargs['positional'] = args[-1][0] != '-'
    #     self._arguments[key] = kwargs

    @property
    def docstring(self):
        self._arguments['help'] = self._arguments.pop('help')
        data = []
        for key, args in self._arguments.items():
            data.append('.. option:: ')
            action = args.get('action', 'store')
            for flag in args['flags']:
                data.append(flag)
                if not args['positional'] and action in ('store', 'append'):
                    data.append(f' <{key}>')
                data.append(', ')
            data[-1] = '\n\n'
            data.append(f'  {args["help"][0].upper()}{args["help"][1:]}.\n\n')
        return ''.join(data)

PARSER = Parser(
    prog='idml2docbook',
    description='Convert IDML files to DocBook.',
    usage='%(prog)s [options]')
PARSER.add_argument(
    'input', help='filename of the IDML input')
PARSER.add_argument(
    '-x', '--idml2hubxml_file', action='store_true',
    help='consider this file as a hubxml file, '
    'this can be handy to gain computing time if you '
    'have already performed idml2xml on your IDML source file')
PARSER.add_argument(
    '-o', '--output', type=str,
    help='filename where output is written, defaults to stdout')
PARSER.add_argument(
    '-m', '--map', type=str,
    help='filename of the JSON map file to perform role-specific actions, '
    'reads by default the value of the .env file')
PARSER.add_argument(
    '-g', '--hierarchy', action='store_true',
    help='do not generate nested sections out of a flat hierarchy, '
    'works in pair with --map')
PARSER.add_argument(
    '-c', '--cut', action='store_true',
    help='cut the input file in several output files '
    'works in pair with --map (for specifying the cuts), '
    'if used with --output, output is considered as a folder.')
PARSER.add_argument(
    '-n', '--names', action='store_true',
    help='infer output file names based on the sections ids, '
    'only used in pair with --cut')
PARSER.add_argument(
    '-t', '--typography', action='store_true',
    help='do not redo the orthotypography (thin spaces, nbsp...)')
PARSER.add_argument(
    '-b', '--linebreaks', action='store_true',
    help='do not replace <br> tags with spaces')
PARSER.add_argument(
    '-p', '--prettify', action='store_true',
    help='prettify the DocBook output, '
    'warning: may add unwanted spaces in your output!')
PARSER.add_argument(
    '-f', '--media', type=str,
    help='path to the media folder, defaults to "Links"')
PARSER.add_argument(
    '-r', '--raster', type=str,
    help='extension to replace raster media files extensions with, '
    'e.g. "jpg", defaults to None')
PARSER.add_argument(
    '-v', '--vector', type=str,
    help='extension to replace vector media files extensions with, '
    'e.g. "svg", defaults to None')
PARSER.add_argument(
    '-i', '--idml2hubxml-output', type=str,
    help='path to the output of Transpect’s idml2hubxml converter, '
    'defaults to "idml2hubxml"')
PARSER.add_argument(
    '-s', '--idml2hubxml-script', type=str,
    help='path to the script of Transpect’s idml2xml converter, '
    'reads by default the value of the .env file')
PARSER.add_argument(
    '--version', action='version',
    version=f'idml2docbook version {__version__}',
    help='print idml2docbook’s version number and exit')
PARSER.set_defaults(**DEFAULT_OPTIONS)

def main(argv=None, stdout=None, stdin=None):
    args = PARSER.parse_args(argv)
    logging.debug("Parsed command-line arguments: " + str(args))

    options = {
        key: value for key, value in vars(args).items() if key in DEFAULT_OPTIONS
    }

    docbook = idml2docbook(args.input, **options)
    
    if(args.cut):
        names, sections = split_docbook(docbook, **options)
        if(args.output):
            logging.info("Creating directory if it does not exist: " + args.output)
            os.makedirs(args.output, exist_ok=True)
            for i, section in enumerate(sections):
                filename = args.output + "/{:02d}_".format(i)

                if(args.names): filename = filename + names[i] + ".xml"
                else: filename = filename + "cut.xml"

                logging.info("Writing file: " + filename)
                with open(filename, "w") as file:
                    file.write(section)
        else:
            for i, section in enumerate(sections):
                print(section)
    else:
        if(args.output):
            logging.info("Writing file: " + args.output)
            with open(args.output, "w") as file:
                file.write(docbook)
        else: print(docbook)

if __name__ == "__main__":
    main()