# This is a set of functions which can be used in other projects to set up
# logging and catch any unhandled exceptions.
import sys
import os
import json
import logging
from logging import StreamHandler

# https://github.com/ulule/python-logstash-formatter
from logstash_formatter import LogstashFormatterV1

# https://github.com/eht16/python-logstash-async
from logstash_async.handler import AsynchronousLogstashHandler

# see the example:
# https://github.com/eht16/python-logstash-async/blob/master/example1.py

app_name = os.getenv('APPLICATION_NAME', __name__)
logstash_host = os.getenv('LOGSTASH_HOST', 'localhost')
logstash_port = int(os.getenv('LOGSTASH_PORT', 5959))
database_path = os.getenv('LOGSTASH_DB_PATH', 'logstash.db')


def get_handler(extra={}):
    extra['logstash_host'] = logstash_host
    extra['logstash_port'] = logstash_port
    formatter = LogstashFormatterV1(fmt=json.dumps({"extra": extra}))
    handler = AsynchronousLogstashHandler(logstash_host, logstash_port,
                                          database_path=database_path)
    handler.setFormatter(formatter)
    return handler


def logstash_init(loggername, extra={}):
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_handler(extra))
    logger.addHandler(StreamHandler(stream=sys.stdout))
    return logger


my_logger = logstash_init(app_name)


# this part is from SO:
# https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    xinfo = (exc_type, exc_value, exc_traceback)
    my_logger.error("Uncaught exception (sys.excepthook handler)",
                    exc_info=xinfo)


# don't forget to set the sys handler:
sys.excepthook = handle_exception
