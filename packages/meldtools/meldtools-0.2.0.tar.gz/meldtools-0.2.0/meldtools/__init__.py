'''Interact with MELD corpus in Python

Load MELD corpus files and intract with their contents using
Python REPL or use it as an object in your own scripts.
'''

# Standard library imports
from pathlib import Path
from typing import Dict, List, Optional, Union

# Local imports
from meldtools.handlers import list_dir, load_meta
from meldtools.models import Meld, MeldDocument


__version__ = '0.2'


def load(directory: str, register: Optional[str] = None) -> Meld:
    '''Load MELD corpus as a Meld object

    The function retrieves all text files found in a specified directory.
    Files are then opened and turned into MeldDocument objects that are
    then attached to a Meld object serving as an interface to
    interact with the text and possibly meta data stored at each MeldDocument.

    Args:
        directory: directory keeping the MELD base files
        register: CSV file with MELD metadata

    Returns:
        a Meld object with MELD documents found in the directory
    '''
    filepaths: List[Path] = list_dir(directory)
    if register:
        metadata: Dict[str, Dict[str, Union[str, float]]] = load_meta(register)
    meld = Meld()

    for path in filepaths:
        with open(path) as f:
            try:
                # Kent_DXXX_* the 2nd part fo the file name has the code
                identifier = path.stem.split('_')[1]
                meta = metadata.get(identifier, None)
                if meta:
                    meta['meld_code'] = identifier
            except NameError:
                meta = None
            doc = MeldDocument(f.read(), path, metadata=meta)
            meld.append(doc)
    return meld
