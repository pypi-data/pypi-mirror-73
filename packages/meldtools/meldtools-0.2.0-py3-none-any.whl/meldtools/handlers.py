'''Input handling and opening MELD corpus files'''

# Standard library imports
from functools import partial
import os
from pathlib import Path
import re
from typing import Callable, Dict, List, Optional, Union

# Non-standard library imports
import pandas as pd  # type: ignore
from pandasql import sqldf  # type: ignore


MELD_TEXT_SUFFIX = '.txt'


def list_dir(directory: str) -> List[Path]:
    '''Recursively list all MELD text files in a directory

    Args:
        directory: directory to traverse

    Returns:
        list of MELD text files as Path objects
    '''
    result: List[Path] = []
    for e in Path(directory).rglob(f'*{MELD_TEXT_SUFFIX}'):
        result.append(e.resolve())
    return sorted(result)


def load_meta(register: str) -> Dict[str, Dict[str, Union[str, float]]]:
    '''Read a CSV file into a Dict with MELD codes as keys

    Args:
        register: CSV file with metadata

    Returns:
        metadata parsed into a Dict with MELD codes as indecies
    '''
    df_meta = pd.read_csv(register)
    meld_codes = sqldf('SELECT * FROM df_meta ORDER BY meld_code', locals())
    return meld_codes.set_index('meld_code').to_dict('index')


def concify(text: str) -> str:
    '''Convert MELD diplomatic transcription to the conc version

    Pre-defined regular expression replacement pipeline that turns text
    contents of the Base MELD file to its Conc counterpart.

    Comments:
    * Text in the Base format must not have tags spanning across
      multiple lines.
    * Symbols that are not intended to form a part of a word must not
      be kept separate in the CONC version.

    Arrangement:
    1.  Remove header
    2.  Remove foliation and pagination marks
    3.  Remove comment tags
    4.  Remove standalone tags, e.g. <ct>
    5.  Remove enclosing <rub>, <addr> and <sgn> tags
    6.  Remove enclosing <und> and <sub> tags
    7.  Remove percent sign
    8.  Replace <lat> and <fre> tags with the pound sign
    9.  Replace tags related to text removed by a scribe with ¤
    10. Append closing braces to each word and remove enclosing tag
    11. Append opening braces to each word and remove enclosing tag
    12. Remove commas
    13. Replace colon with semi-colon
    14. Replace plus with underscore
    15. Delete <?> question tags and all other question marks
    16. Replace start char (*) with colon
    17. Replace @ with ~
    18. Sort out word division:
        - take the 1st part of the word from line 1
        - capture = to keep it if it is present
        - subsitute intermediate # with [
        - take the 2nd part of the word from line 2
        - if exists, place = before [
        - move the 2nd part to line 1
        - add a newline character at the word
    19. Remove : between characters (inside the word)
    20. Remove empty lines
    21. Remove trailing and leading whitespace
    22. Replace multiple horizontal whitespace characters with a single one

    Args:
        text: contents of the MELD document in Base (diplomatic) version

    Returns:
        text contents of the MELD document converted to the Conc version
    '''
    head = ChainNode(r'^<(c(ounty|ode)|function|ms\.|proofread|reference'
                     r'|t(ext|ranscribed|ranche))( by){0,1}:.*?>$',
                     re.IGNORECASE | re.MULTILINE)
    second = ChainNode(r'\[.*?\]')
    third = ChainNode(r'<com>.*?</com>')
    fourth = ChainNode(r'<(ct|fil|gap|hole|mng'
                       r'|nta|pos|pph|spa|spn|sic|uis)>', re.IGNORECASE)
    fifth = ChainNode(r'<(rub|addr|sgn)>(.*?)</\1>', repl=r'\2')
    sixth = ChainNode(r'<(und|sub)>(.*?)</\1>', repl=r'\2')
    seventh = ChainNode('%')
    eight = ChainNode(r'<(?:lat|fre)>.*?</(?:lat|fre)>', repl='£ ')
    ninth = ChainNode(r'<(cor|exp|rbd|ill)>.*?</\1>', repl='¤ ')
    tenth = ChainNode(r'<(?:sup|add|mrg)>(.*?)</(?:sup|add|mrg)>',
                      repl=partial(_append_to_word, '}'))
    eleventh = ChainNode(r'<cro>(.*?)</cro>', repl=partial(_append_to_word, '{'))
    twelfth = ChainNode(r',')
    thirteeth = ChainNode(r':', repl=';')
    fourteenth = ChainNode(r'\+', repl='_')
    fifteenth = ChainNode(r'<?\?>?')
    sixteenth = ChainNode(r'\*', repl=':')
    seventeenth = ChainNode('@', repl='~')
    eighteenth = ChainNode(r'([\w{}:_~\\-]+)(=?)(#\n)(.*?)\s', repl=r'\1\2[\4\n')
    nineteenth = ChainNode(r'(([([\w{}:_~\\-])(:))', repl=r'\2')
    twentieth = ChainNode(r'^(?:[\t ]*(?:\r?\n|\r))+')
    twenty_first = ChainNode(r'[\t ]+$|^[\t ]+', re.MULTILINE)
    twenty_second = ChainNode(r'[\t ]{2,}', repl=' ')
    head.join(second).join(third).join(fourth).join(fifth).join(sixth).\
        join(seventh).join(eight).join(ninth).join(tenth).join(eleventh).\
        join(twelfth).join(thirteeth).join(fourteenth).join(fifteenth).\
        join(sixteenth).join(seventeenth).join(eighteenth).join(nineteenth).\
        join(twentieth).join(twenty_first).join(twenty_second)
    return head(text)


def _append_to_word(symbol: str, matchobj: re.Match) -> str:
    '''Append symbol at the end of each word in the match group

    Args:
        symbol: the character to be appended at the end of the word
        matchobj: the captured regular expression group

    Returns:
        the processed string
    '''
    skipped = ['¤', '£', '{', '}', '<', '>', '.']
    result = ' '.join([w+symbol if not any((c in skipped) for c in w) else w
                      for w in matchobj.groups()[0].split()])
    return result


class ChainError(Exception): ...


class ChainNode:
    '''An element in a chain of operations with regular expressions

    Args:
        regexp: regex pattern to match
        *flags: regex flags, e.g., ignorecase or multiline
        repl: replacement for the regex pattern
    '''
    def __init__(self, regexp: str, *flags, repl: Union[str, Callable] = '') -> None:
        try:
            self.regexp = re.compile(regexp, *flags)
        except re.error:
            raise ChainError(f'Faulty regex {regexp} \
                               failed to instantiate {self.__class__.__name__}.')
        self.repl = repl
        self._next_node: Optional[ChainNode] = None
        '''The following node in the chain of operations with regular expressions'''

    def __call__(self, text: str) -> str:
        '''Simplify the method call for prebuilt chains

        For instance, concify(text) is more equally informative
        as the handle() function call.

        Args:
            text: text contents of a MELD document

        Returns:
            text after changes
        '''
        return self.handle(text)

    def join(self, node: 'ChainNode') -> 'ChainNode':
        '''Get the next node in the chain

        Args:
            node: next node in a chain of execution

        Returns:
            the attached node
        '''
        self._next_node = node
        return node

    def handle(self, text: str) -> str:
        '''Perform substitution with a regular expression

        Args:
            text: text contents of a MELD document

        Returns:
            text after changes
        '''
        text = self.regexp.sub(self.repl, text)
        if self._next_node:
            return self._next_node.handle(text)
        return text
