#!/usr/bin/env python3
''' A module for filtering logs.
'''

import re
from typing import List
import logging
from typing import Tuple
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' Creates a connector to a mysql database.
    '''
    connection = mysql.connector.connect(
                host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
                port=3306,
                user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
                password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
                database=os.getenv('PERSONAL_DATA_DB_NAME', ''),
                )

    return connection


def get_logger() -> logging.Logger:
    ''' Creates a new logger for user data.
    '''
    logger = logging.getLogger('user_data')
    logger.setLevel(loggging.INFO)

    # Create a StreamHandler and set its level to INFO
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    # Create a RedactingFormatter with PII_FIELDS
    formatter = RedactingFormatter(PII_FIELDS)

    # Set the formatter for the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Disable propagation to other loggers
    logger.propagate = False

    return logger


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


def main():
    """Logs the information about user records in a table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)
