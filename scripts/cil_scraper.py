"""
# cil_finder.py
# @author Ian Effendi
#
# Scrapes https://www.ilru.org/projects/cil-net/cil-center-and-association-directory-results/<state> and outputs results in *.csv or *.json format.
"""

import os
import pathlib
import sys, json, csv
import argparse
from types import FunctionType
import scrapy

from collections import namedtuple
from typing import Any, List, Set, Dict, IO, TextIO, BinaryIO, Union, no_type_check
from tqdm import tqdm

# Example constants.
Constants = namedtuple('Constants', ['program', 'bob', 'handy'])
constants = Constants("IRLU <CIL Scraper>",
                      {     
                        "name": { 
                            "first": "Bob",
                            "last": "Builder",
                        },
                        "age": 20,
                        "email": "bob.builder@example.com"
                      }, 
                      {
                        "name": {
                            "first": "Handy",
                            "last": "Manny",
                        },
                        "age": 18,
                        "email": "handy.manny@example.com"
                      })

parser = argparse.ArgumentParser(prog=constants.program, description="Scrape webpage content from ILRU Directory of Centers for Independent Living (CILs) and Associations.")
"""Argument parser object used to enable command line interactions."""

###########################
# COMMAND-LINE ARGUMENTS
###########################

# --version argument.
parser.add_argument("--version", action='version', version='%(prog)s 0.1.0')

# --verbose argument.
parser.add_argument("-v", "--verbose",
                    help="Increase output verbosity.", 
                    action='count', default=0)

# --dry argument.
parser.add_argument('-D', '--dry', action='store_true',
                    help="Run output without making requests or saving results.")

# Scraper grouped arguments.
spider_options = parser.add_argument_group('Spider Options', 'Arguments used to control the scraper bot.')

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
output_options = parser.add_argument_group('Output Options', 'Arguments used to control the output.')

# --format argument. Used to specify JSON or CSV output.
output_options.add_argument('-f', '--format', metavar='FORMAT', dest="formats",
                    action="append", choices=['csv', 'tsv', 'json', 'stdout'], 
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

# --output argument. Used to specify single output file that doesn't consider other extensions.
output_options.add_argument('-o', '--output', metavar="FILE", dest="files",
                            action="append", type=argparse.FileType('wt', encoding='UTF-8'),
                            help="Save single output to provided locations.")

# --filename argument. Used to specify a filename that should be used with the extensions.
output_options.add_argument('-n', "--name", metavar="FILENAME", dest="filenames",
                            action="append",
                            help="Save files with this filename, one for every extension option provided.")

# --testing argument. Used to specify testing.
parser.add_argument('--test', dest="testing",
                    action="store_true", default=False,
                    help=argparse.SUPPRESS)

# Parse the arguments
cargs = parser.parse_args()

def verbose_printer(threshold: int) -> FunctionType:
    """Decorator factory for creating verbose threshold printers."""
    if threshold is None:
        threshold = 0
    def wrapped_printer(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """Forward arguments to print() method, if verbose threshold exceeded.
        """
        # Check again if verbosity is changed during runtime.
        if cargs.verbose and cargs.verbose >= threshold:
            print(*args, **kwargs)
            
    if cargs.verbose and cargs.verbose >= threshold:
        # Return wrapped print function.
        return wrapped_printer
    else:
        # Empty function.
        return lambda _ : 0

# Setup the print statements.
# printa  = verbose_printer(threshold=0)
printv  = verbose_printer(1)
printvv = verbose_printer(2)
    
# Verify to user the verbose level.
printv(f"Executing {constants.program} in verbose mode (level={cargs.verbose})...")

# If verbose and dry:
if cargs.dry:
    printv(f'--dry is {cargs.dry}. Output will not be saved.')

###########################
# COMMAND-LINE ARGUMENT DEDUPLICATIONS
###########################

# Deduplicate array.
def deduplicate(array: List[Any], required:bool=False) -> Set:
    """Deduplicate arbitrary amount of items in a list.

    :param array: Array to deduplicate.
    :type array: List[Any]
    :param required: Flag determining if required argument is missing.
    :type required: bool
    :raises argparse.ArgumentError: Raised if required argument is missing.
    :return: Return deduplicated collection.
    :rtype: Set
    """
    if not array:
        if required:
            printvv("Missing required parameter.")
            raise ValueError("Missing at least one required parameter.")
        printvv("\tSkipping. Nothing to deduplicate.")
        return set()
    else:
        n_duplicates = len(array)
        printvv(f'\tReceived: {array}.')
        deduplicated_set = set(array)
        n = len(deduplicated_set)
        if(n_duplicates != n):
            printvv(f'\tResult: {deduplicated_set} - Removed {n_duplicates - n} duplicate(s)')
        else:
            printvv(f'\tArguments unchanged. No duplicates to remove.')
        return deduplicated_set

# Manually control tqdm.
with tqdm(total=4, position=0) as dedupe_pbar:

    # Update bar description.
    dedupe_pbar.set_description(f'Deduplicating arguments...')
    
    # Deduplicate states.
    printvv(f'\nRemoving duplicate states...')
    cargs.states = deduplicate(cargs.states, required=True)
    dedupe_pbar.update(1)

    # Deduplicate formats.
    printvv(f'Removing duplicate formats...')
    cargs.formats = deduplicate(cargs.formats, required=False)
    dedupe_pbar.update(1)

    # Deduplicate filenames.
    printvv(f'Removing duplicate filenames...')
    cargs.filenames = deduplicate(cargs.filenames, required=False)
    dedupe_pbar.update(1)

    # Deduplicate files.
    printvv(f'Removing duplicate files...')
    cargs.files = deduplicate(cargs.files, required=False)
    dedupe_pbar.update(1)

###########################
# FILE WRITERS
###########################

def make_qualified_filename(basename: str = "output", state: str = "UNKNOWN", sep: str = ".", prefix: str = "", suffix: str = "") -> str:
    """Create filename using specified components.

    :param basename: Base of the filename.
    :type basename: str
    :param state: State code to add to the filename.
    :type state: str
    :param sep: Separator to use between prefix and suffix components on the file, defaults to "."
    :type sep: str, optional
    :param prefix: Prefix to apply to the file, defaults to empty str
    :type prefix: str, optional
    :param suffix: Suffix to apply to the file, defaults to emtpy str
    :type suffix: str, optional
    :return: Return qualified filename.
    :rtype: str
    """
    if state is None:
        state = "UNKNOWN"
    if basename is None:
        basename = "output"
    basename = f'{state}{sep}{basename}'
    if prefix:
        prefix = f'{prefix}{sep}'
    if suffix:
        suffix = f'{sep}{suffix}'
    filename = f'{prefix}{basename}{suffix}'
    printvv(f'Generated qualified filename: {filename}')
    return filename

def content_writer(writer_func: FunctionType) -> FunctionType:
    def wrapper(file: IO, content: Any, params: Dict[str, str] = {}, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        # If no content, exist.
        if not content:
            printvv(f'No content to write...')
            return
        
        # If open file is provided and is writable, write content to it.
        if file:
            printvv(f"Explicit file provided...")
            printvv(f"Writing content to {os.path.basename(file.name)}")
            result = writer_func(file, content, *args, **kwargs)
            return
        
        # Get explicit filename or make the filename from provided components.
        filename = params.get('filename', make_qualified_filename(**params))
        
        # If no file, fall back to filename.
        if filename:
            printvv(f"Opening file: {filename}...")
            with open(filename, 'w', newline='') as uri:
                printvv(f"Writing content to {os.path.basename(uri.name)}")
                result = writer_func(uri, content, *args, **kwargs)
                return result
        
        # No filename and no file.
        printvv("Unable to write content. No file provided.")
        return            
    return wrapper

@content_writer
def to_json(file: IO, content: List[Any], **kwargs: Dict[str, Any]) -> None:
    """Write JSON-formatted content out to provided file.

    :param file: File-like object to write JSON to.
    :type file: IO
    :param content: Content to be serialied into JSON.
    :type content: Any
    """    
    json.dump(content, file, **kwargs)
        
def print_json(content: Any, **kwargs: Any) -> None:
    """Write JSON-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by json.dump()
    """
    printvv("Exporting results to the standard output.")
    to_json(sys.stdout, content, **kwargs)
    print("")

@content_writer
def to_csv(file: IO, content: List[Dict[Any, Any]], **kwargs: Dict[str, Any]) -> None:
    """Write CSV-formatted content out to provided file.

    :param file: File-like object to write CSV to.
    :type file: IO
    :param content: Content with a set of fields and rows to serialize into CSV.
    :type content: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    """
    # If content is a single dictionary, assign to single-element list.
    if isinstance(content, dict):
        content = [ content ]

    # Create CSV writer.
    csv_writer = csv.DictWriter(file, content[0].keys(), **kwargs)
     
    # Include headers by default. Set headers=False in order to skip header row.

    if kwargs.get("headers", True):
        csv_writer.writeheader()
        printvv(f"Wrote header with {len(csv_writer.fieldnames)} field(s).")
    
    # If not verbose, write and exit.
    if not cargs.verbose:
        csv_writer.writerows(content)
        return
    
    # If verbose, print messages.
    if cargs.verbose:    
        n_rows = 0
        for row in content:
            n_rows += 1
            csv_writer.writerow(row)                
            printvv(f"Wrote row {n_rows}: {row}")
                
def print_csv(content: Dict[Any, Any], **kwargs: Any) -> None:
    """Write CSV-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by csvwriter()
    """
    printvv("Exporting results to the standard output.")
    to_csv(sys.stdout, content, **kwargs)
    print("")
                
@content_writer
def to_tsv(file: IO, content: List[Dict[Any, Any]], **kwargs: Dict[str, Any]) -> None:
    """Write TSV-formatted content out to provided file.

    :param file: File-like object to write TSV to.
    :type file: IO
    :param content: Content with a set of fields and rows to serialize into TSV.
    :type content: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    """
    to_csv(file, content, delimiter='\t', **kwargs)
    
def print_tsv(content: Dict[Any, Any], **kwargs: Any) -> None:
    """Write TSV-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by csvwriter()
    """
    printvv("Exporting results to the standard output.")
    to_tsv(sys.stdout, content, **kwargs)
    print("")
                
###########################
# EARLY EXIT IF --dry
###########################

if cargs.dry:
    printvv("End of execution. No changes made to the filesystem.")
    sys.exit()
    
###########################
# TESTS
###########################

def get_flattened_content(data):
    return {
        "first.name": data['name']['first'],
        "last.name": data['name']['last'],
        "age": data['age'],
        "email": data['email'],
    }

def get_content():
    return [
        get_flattened_content(constants.bob),
        get_flattened_content(constants.handy)
    ]
    
###############
# STDOUT TESTS

def test_print_json():
    printvv()
    printvv("Testing JSON to stdout.")
    print_json(constants.bob)
    print_json(constants.handy)
    
def test_print_csv():
    printvv()
    printvv("Testing CSV to stdout.")
    print_csv(get_content())
    
def test_print_tsv():
    printvv()
    printvv("Testing TSV to stdout.")
    print_tsv(get_content())
    
###############
# FILE TESTS

def test_output_json():
    printvv()
    printvv("Testing JSON file output.")
    content = [ constants.bob, constants.handy ]
    to_json(None, content, params={ "basename": cargs.filenames, 
                                   "state": "ca", 
                                   "prefix": "test", 
                                   "suffix": "json" })

def test_output_csv():    
    printvv()
    printvv("Testing CSV file output.")
    content = get_content()
    to_csv(None, content, params={ "basename": "output", 
                                   "state": "ny", 
                                   "prefix": "test", 
                                   "suffix": "csv" })
    
def test_output_tsv():  
    printvv()  
    printvv("Testing TSV file output.")
    content = get_content()
    to_tsv(None, content, params={ "basename": "output", 
                                   "state": "oh", 
                                   "prefix": "test", 
                                   "suffix": "tsv" })

if cargs.testing:
    
    # Setup tests.
    tests = [
        test_print_json,
        test_print_csv,
        test_print_tsv,
        test_output_json,
        test_output_csv,
        test_output_tsv
    ]
    
    # Print progress.
    printv()
    with tqdm(tests, position=0) as tests_pbar:
        tests_pbar.set_description("Executing tests...")
        print()
        for test in tests_pbar:
            test()
            
    sys.exit()
    
###########################
# EXECUTE SPIDER
###########################

###########################
# OUTPUT DATA TO FILE
###########################