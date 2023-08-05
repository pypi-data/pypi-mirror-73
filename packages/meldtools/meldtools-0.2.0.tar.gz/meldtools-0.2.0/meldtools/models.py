'''Data models used in MELD tools'''

# Standard library imports
from collections import defaultdict
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Dict, DefaultDict, Generator, List, Optional, Set, Union

# Local imports
from .handlers import concify


# TODO: add function to recover ngrams, as a list of vectors [_, hello, world, _]


class MeldIndexationError(Exception): ...


@dataclass
class MeldJsonSchema:
    '''Schema specifying how a MELD document is represented in JSON'''
    meld_code: str
    date: Union[int, float]
    period: str
    latitude: float
    longitude: float
    format: str
    function_primary: str
    function_secondary: str
    conc: str


class MeldDocument:
    '''Single document from the MELD corpus

    Attributes:
        text: contents of the document
        filename: resolved POSIX path to the file
        lines: contents of the document split into lines
        conc: contents of the document in the CONC format
        meta: metadata associated with the document
        X: metadata dictionary keys are accessible as instance attributes

        self._lines: underlying list of lines
        self._conc: underlying text in the CONC format
    '''
    def __init__(self, text: str, filename: Path = None, *,
                 metadata: Dict[str, Union[str, float]] = None) -> None:
        self.text = text
        self.filename = filename
        self._lines: Optional[List[str]] = None
        self._conc: Optional[str] = None
        self.meta: Dict[str, Union[str, int, float]] = {}

        # Expose metadata as instance attributes
        if metadata:
            for key, value in list(metadata.items()):
                if value != value: # Check for NaN (Not a number)
                    value = 0.0
                elif (num := self._is_number(value)):
                    value = num
                setattr(self, key, value)
                self.meta[key] = value

    def __str__(self) -> str:
        '''Get the unique identifier of the MELD document'''
        if self.filename:
            county, code, *_ = self.filename.name.split('_')
            return f'{county}::{code}'
        return 'document::' + str(id(self))

    @property
    def lines(self) -> List[str]:
        '''Retrive the conc attribute as a list of lines'''
        if self._lines is None:
            self._lines = self.conc.split('\n')
        return self._lines

    @property
    def conc(self) -> str:
        '''Retrive the contents of the MELD document in CONC format'''
        if not self._conc:
            self._conc = concify(self.text)
        return self._conc

    def _is_number(self, value: Union[str, float]) -> Union[float, int, bool]:
        '''Check if the value can be converted to a numerical type

        Args:
            value: the variable to be checked

        Returns:
            either the value converted to a numerical type or False
        '''
        try:
            # inf means 'inferred' in the MELD context
            if value == 'inf':
                raise ValueError

            result = float(value)
        except (ValueError, TypeError):
            return False
        else:
            if result.is_integer():
                return int(result)
            return result


class Meld:
    '''Dataclass for multiple MELD documents

    Attributes:
        self._docs: list of MeldDocuments read from MELD base file(s)
        self._meta: underlying dictionary of metadata
    '''
    def __init__(self):
        self._docs: List[MeldDocument] = list()
        self._meta: Optional[DefaultDict[str, Set[Union[str, int, float]]]] = None

    def __iter__(self) -> Generator[MeldDocument, None, None]:
        '''Allow to iterate over MeldDocument objects'''
        for d in self._docs:
            yield d

    def __len__(self) -> int:
        '''Provide the number of MELD documents stored in the container'''
        return len(self._docs)

    def __getitem__(self, i: Union[slice, int]) -> Union[List[MeldDocument], MeldDocument]:
        '''Indexing and slicing protocol for the underlying _docs

        Args:
            i: index or a slice defining the range

        Returns:
            MeldDocument instance at a given index or a slice of MeldDocuments

        Raises:
            MeldIndexationError: the error is raised whenver index is not int
                                 or slice is wrong
        '''
        try:
            if isinstance(i, slice):
                return self._docs[i.start : i.stop : i.step]
            return self._docs[i]
        except (IndexError, TypeError):
            raise MeldIndexationError('Document index out of range.')

    @property
    def meta(self) -> Optional[DefaultDict[str, Set[Union[str, int, float]]]]:
        '''Retrieve metadata from MeldDocument object

        Returns:
            dictionary with metadata attributes and possible values
        '''
        if self._meta is None:
            self._meta = defaultdict(set)

            for d in self:
                if d.meta:
                    for k, v in d.meta.items():
                        self._meta[k].add(v)

        return self._meta

    def append(self, doc: MeldDocument) -> None:
        '''Append MELD document to the underlying _docs'''
        self._docs.append(doc)

    def extend(self, docs: List[MeldDocument]) -> None:
        '''Extend the underlying _docs with a list of MELD documents'''
        self._docs.extend(docs)

    def search(self, key: str, values: List[Union[str, int]]) -> 'Meld':
        '''Retrieve a copy of Meld object with a subset of documents

        It limits the scope of documents to a particular subset
        sharing the values for a given key.

        Values have to match the key if anything else but an empty
        Meld object is to be returned. For example, the key 'function'
        can be matched with values such as 'lease' or 'memorandum' but
        not '1400'.

        Time scope can be specified as a list like this: [1399, 1525].

        Args:
            key: metadata attribute to be searched
            values: expected values for the metadata attribute

        Returns:
            a Meld object with a subset of documents
        '''
        meld_copy = self.__class__()
        docs: List[MeldDocument] = []
        for doc in self._docs:
            try:
                if key == 'date':
                    try:
                        date = int(getattr(doc, key))
                        if date >= int(values[0]) and date <= int(values[1]):
                            docs.append(doc)
                    except ValueError:
                        continue
                else:
                    if getattr(doc, key) in values:
                        docs.append(doc)
            except AttributeError:
                continue
        meld_copy.extend(docs)
        return meld_copy
