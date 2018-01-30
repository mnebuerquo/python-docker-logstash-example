from flask import request, has_request_context
from logsetup import get_formatter

fields = [
        'form',
        'args',
        'cookies',
        'headers',
        'data',
        'method',
        'url',
        'full_path',
        'is_xhr',
        'is_json',
        'module',
        'remote_addr'
        ]

class RequestFormatter():

    def __init__(self, extra={}):
        self.formatter = get_formatter(extra)

    def format(self, record):
        if has_request_context():
            for field in fields:
                record[field] = request[field]
        return self.formatter.format(record)
