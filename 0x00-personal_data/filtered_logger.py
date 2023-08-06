#!/usr/bin/env python3
''' A module for filtering logs.
'''

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' Filters/obfuscate a log message.
    '''
    pattern = r'(' + '|'.join(map(re.escape, fields)) +\
              r')=(.*?)(?=' + re.escape(separator) + '|$)'
    return re.sub(pattern, rf'\1={redaction}', message)
