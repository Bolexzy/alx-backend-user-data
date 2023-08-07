#!/usr/bin/env python3
''' A module for filtering logs.
'''

import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formats a LogRecord.
        '''
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' Filters/obfuscate a log message.
    '''
    pattern = r'(' + '|'.join(map(re.escape, fields)) +\
              r')=(.*?)(?=' + re.escape(separator) + '|$)'
    return re.sub(pattern, rf'\1={redaction}', message)
