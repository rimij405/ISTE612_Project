"""
# arguments.py
# @author Ian Effendi
#
# Provides prepared argument parser for the scraper.
"""

import argparse
from . import constants

argparser = argparse.ArgumentParser(prog=constants.program, description="Scrape webpage content from ILRU Directory of Centers for Independent Living (CILs) and Associations.")
"""Argument parser object used to enable command line interactions."""

###########################
# COMMAND-LINE ARGUMENTS
###########################

# --version argument.
argparser.add_argument("--version", action='version', version='%(prog)s 0.1.0')

# --verbose argument.
argparser.add_argument("-v", "--verbose",
                    help="Increase output verbosity.", 
                    action='count', default=0)

# --dry argument.
argparser.add_argument('-D', '--dry', action='store_true',
                    help="Run output without making requests or saving results.")

# Scraper grouped arguments.
spider_options = argparser.add_argument_group('Spider Options', 'Arguments used to control the scraper bot.')

# --state argument. Contains input to parse.
spider_options.add_argument('--state', metavar='STATE', dest="states",
                    action='append', choices=['CA', 'OH', 'NY'],
                    help="Scrape results for supplied STATE values.")

# --OH argument.
spider_options.add_argument('-CA', '--CA', dest="states",
                            action="append_const", const="CA",
                            help="Scrape results for CA state.")

# --NY argument. 
spider_options.add_argument('-NY', '--NY', dest="states",
                            action='append_const', const="NY",
                            help="Scrape results for NY state.")

# --OH argument.
spider_options.add_argument('-OH', '--OH', dest="states",
                            action="append_const", const="OH",
                            help="Scrape results for OH state.")

# Output grouped arguments.
output_options = argparser.add_argument_group('Output Options', 'Arguments used to control the output.')

# --output argument. Used to specify single output file that doesn't consider other extensions.
output_options.add_argument('-o', '--output', metavar="FILE", dest="files",
                            action="append", type=str, default=None,
                            help="Save single output to each provided text file provided. Format is inferred by provided input.")

# --sep argument. Used to specify filename component separators.
output_options.add_argument('-sep', '--separator', metavar='SEPARATOR', dest="sep",
                            action="store", type=str, default=".",
                            help="Separator used to separate filename components when generating filenames, defaults to '.'.")

# Prefix exclusions.
prefix_options = output_options.add_mutually_exclusive_group()

# --namespace argument. Used to specify filename component separators.
prefix_options.add_argument('-ns', '--namespace', metavar='NAMESPACE', dest="prefix",
                            action="store", type=str, default="ns",
                            help="Prefix applied to files with generated filenames, defaults to 'ns'.")

# --top-level-domain argument. Used to specify filename component separators.
prefix_options.add_argument('-top', '--top-level-domain', metavar='DOMAIN', dest="prefix",
                            action="store", type=str, default="com", choices=['com', 'gov', 'edu', 'net', 'org', 'io', 'me'],
                            help="Prefix applied to files with generated filenames using a top-level-domain code, defaults to 'com'.")

# --prefix argument. Used to specify filename component separators.
prefix_options.add_argument('-pre', '--prefix', metavar='PREFIX', dest="prefix",
                            action="store", type=str, default="export",
                            help="Prefix applied to files with generated filenames, defaults to 'export'.")

# --format argument. Used to specify JSON or CSV output.
output_options.add_argument('-f', '--format', metavar='FORMAT', dest="formats",
                    action="append", choices=['csv', 'tsv', 'json', 'stdout'], default=None,
                    help="Save results in specified file format.")

# --json argument. Used to specify JSON output.
output_options.add_argument('-J', '--json', dest="formats",
                    action="append_const", const="json",
                    help="Save results in *.json file.")

# --csv argument. Used to specify CSV output.
output_options.add_argument('-C', '--csv', dest="formats",
                    action="append_const", const="csv",
                    help="Save results in *.csv file.")

# --tsv argument. Used to specify TSV output.
output_options.add_argument('-T', '--tsv', dest="formats",
                    action="append_const", const="tsv",
                    help="Save results in *.tsv file.")

# --json argument. Used to specify JSON output.
output_options.add_argument('-S', '--stdout', dest="formats",
                    action="append_const", const="stdout",
                    help="Pipe results to the stdout pipe.")

# --filename argument. Used to specify a file basename that should be used with the extensions.
output_options.add_argument('-n', "--name", "--basename", metavar="FILENAME", dest="filenames",
                            action="append", type=str, default=None,
                            help="Save files with this basename, one for every output format provided.")

###########################
# HIDDEN ARGUMENTS
###########################

# --testing argument. Used to specify testing.
argparser.add_argument('--test', dest="testing",
                    action="store_true", default=False,
                    help=argparse.SUPPRESS)
