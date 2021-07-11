"""
# cil_scraper.py
# @author Ian Effendi
#
# Scrapes https://www.ilru.org/projects/cil-net/cil-center-and-association-directory-results/<state> and outputs results in *.csv or *.json format.
"""

from iste.drse import constants
from iste.drse.arguments import argparser

from iste.utils import verbose, filenames
from iste.utils.duplicates import deduplicate

###########################
# PARSE ARGUMENTS
###########################

# Load in the program argument parser.
cargs, unknown = argparser.parse_known_args()

###########################
# PREPARE LOGGER
###########################

# Setup the loggers.
log   = verbose.logger(cargs, threshold=verbose.levels.NONE)
logv  = verbose.logger(cargs, threshold=verbose.levels.LOW)
logvv = verbose.logger(cargs, threshold=verbose.levels.HIGH)

# Verify to user the verbose level.
logv(f"Executing {constants.program} in verbose mode (level={cargs.verbose})...")

def log_filename_args():
    logvv(f'{cargs.sep} (separator)')
    logvv(f'{cargs.prefix} (namespace)')
    logvv(f'{cargs.states} (tags)')
    logvv(f'{cargs.formats} (formats)')
    logvv(f'{cargs.filenames} (filenames)')
    logvv(f'{cargs.files} (files)')

###########################
# CONFIRM DRY-NESS
###########################

# If verbose and dry:
if cargs.dry:
    logv(f'--dry is {cargs.dry}. Executing in dry mode...')

###########################
# COLLECTIVIZE
###########################

# Set defaults.
cargs.prefix = cargs.prefix if cargs.prefix else ""
cargs.formats = cargs.formats if cargs.formats else []
cargs.filenames = cargs.filenames if cargs.filenames else []
cargs.files = cargs.files if cargs.files else []
cargs.sep = cargs.sep if cargs.sep else ""
log_filename_args()

###########################
# DEDUPLICATE INPUT
###########################

cargs.states = deduplicate(cargs.states, message="Removing duplicate states...", logger=logvv)
cargs.formats = deduplicate(cargs.formats, message="Removing duplicate formats...", logger=logvv)
cargs.filenames = deduplicate(cargs.filenames, message="Removing duplicate output basenames...", logger=logvv)
cargs.files = deduplicate(cargs.files, message="Removing duplicate output files...", logger=logvv)
log_filename_args()

###########################
# GENERATE FILENAMES
###########################

if cargs.filenames:
    logvv('Generating filenames from console arguments:')
    cargs.filenames = filenames.generate_filenames(
                        labels=cargs.filenames,
                        formats=cargs.formats,
                        prefix=cargs.prefix,
                        tags=cargs.states,
                        sep=cargs.sep,
                        logger=logvv
                    )

if not cargs.filenames:
    logv(f'No filename labels provided.')

if not cargs.formats:
    logv(f'No formats provided.')

if not cargs.states:
    logv(f'No states provided.')
    
if not cargs.files:
    logv(f'No output files provided.')
log_filename_args()

###########################
# FILE WRITERS
###########################
""" 


def content_writer(writer_func: FunctionType) -> FunctionType:
    def wrapper(file: IO, content: Any, params: Dict[str, str] = {}, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        # If no content, exist.
        if not content:
            logvv(f'No content to write...')
            return
        
        # If open file is provided and is writable, write content to it.
        if file:
            logvv(f"Explicit file provided...")
            logvv(f"Writing content to {os.path.basename(file.name)}")
            result = writer_func(file, content, *args, **kwargs)
            return
        
        # Get explicit filename or make the filename from provided components.
        filename = params.get('filename', make_qualified_filename(**params))
        
        # If no file, fall back to filename.
        if filename:
            logvv(f"Opening file: {filename}...")
            with open(filename, 'w', newline='') as uri:
                logvv(f"Writing content to {os.path.basename(uri.name)}")
                result = writer_func(uri, content, *args, **kwargs)
                return result
        
        # No filename and no file.
        logvv("Unable to write content. No file provided.")
        return            
    return wrapper

@content_writer
def to_json(file: IO, content: List[Any], **kwargs: Dict[str, Any]) -> None:
    ""Write JSON-formatted content out to provided file.

    :param file: File-like object to write JSON to.
    :type file: IO
    :param content: Content to be serialied into JSON.
    :type content: Any
    ""    
    json.dump(content, file, **kwargs)
        
def print_json(content: Any, **kwargs: Any) -> None:
    ""Write JSON-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by json.dump()
    ""
    logvv("Exporting results to the standard output.")
    to_json(sys.stdout, content, **kwargs)
    print("")

@content_writer
def to_csv(file: IO, content: List[Dict[Any, Any]], **kwargs: Dict[str, Any]) -> None:
    ""Write CSV-formatted content out to provided file.

    :param file: File-like object to write CSV to.
    :type file: IO
    :param content: Content with a set of fields and rows to serialize into CSV.
    :type content: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    ""
    # If content is a single dictionary, assign to single-element list.
    if isinstance(content, dict):
        content = [ content ]

    # Create CSV writer.
    csv_writer = csv.DictWriter(file, content[0].keys(), **kwargs)
     
    # Include headers by default. Set headers=False in order to skip header row.

    if kwargs.get("headers", True):
        csv_writer.writeheader()
        logvv(f"Wrote header with {len(csv_writer.fieldnames)} field(s).")
    
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
            logvv(f"Wrote row {n_rows}: {row}")
                
def print_csv(content: Dict[Any, Any], **kwargs: Any) -> None:
    ""Write CSV-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by csvwriter()
    ""
    logvv("Exporting results to the standard output.")
    to_csv(sys.stdout, content, **kwargs)
    print("")
                
@content_writer
def to_tsv(file: IO, content: List[Dict[Any, Any]], **kwargs: Dict[str, Any]) -> None:
    ""Write TSV-formatted content out to provided file.

    :param file: File-like object to write TSV to.
    :type file: IO
    :param content: Content with a set of fields and rows to serialize into TSV.
    :type content: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    ""
    to_csv(file, content, delimiter='\t', **kwargs)
    
def print_tsv(content: Dict[Any, Any], **kwargs: Any) -> None:
    ""Write TSV-formatted stream to standard output.

    :param content: Object to serialize.
    :type content: Any
    :param kwargs: Keyword arguments accepted by csvwriter()
    ""
    logvv("Exporting results to the standard output.")
    to_tsv(sys.stdout, content, **kwargs)
    print("")
                
###########################
# EARLY EXIT IF --dry
###########################

if cargs.dry:
    logvv("End of execution. No changes made to the filesystem.")
    sys.exit()
    
###########################
# TESTS
###########################

if cargs.testing:

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
        logvv()
        logvv("Testing JSON to stdout.")
        print_json(constants.bob)
        print_json(constants.handy)
        
    def test_print_csv():
        logvv()
        logvv("Testing CSV to stdout.")
        print_csv(get_content())
        
    def test_print_tsv():
        logvv()
        logvv("Testing TSV to stdout.")
        print_tsv(get_content())
        
    ###############
    # FILE TESTS

    def test_output_json():
        logvv()
        logvv("Testing JSON file output.")
        content = [ constants.bob, constants.handy ]
        params = [ { k: v for k,v in file.items() } for file in generated_filenames if file['basename']]
        
        
        to_json(None, content, params={ "basename": "output", 
                                    "state": "ca", 
                                    "prefix": "test", 
                                    "suffix": "json" })

    def test_output_csv():    
        logvv()
        logvv("Testing CSV file output.")
        content = get_content()
        to_csv(None, content, params={ "basename": "output", 
                                    "state": "ny", 
                                    "prefix": "test", 
                                    "suffix": "csv" })
        
    def test_output_tsv():  
        logvv()  
        logvv("Testing TSV file output.")
        content = get_content()
        to_tsv(None, content, params={ "basename": "output", 
                                    "state": "oh", 
                                    "prefix": "test", 
                                    "suffix": "tsv" })

    
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
    logv()
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
########################### """