#!/usr/bin/env python3
"""
Log formatter
"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(s, record: logging.LogRecord) -> str:
        """Logging formatter"""
        ms = filter_datum(s.fields, s.REDACTION, record.msg, s.SEPARATOR)
        return s.FORMAT % {'name': record.name, 'message': ms,
                           'levelname': record.levelname,
                           'asctime': s.formatTime(record)}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function that returns a log message obfuscated"""
    for field in fields:
        message = re.sub('(?<={}=)(.*?)(?={})'.format(field, separator),
                         redaction, message)
    return message
