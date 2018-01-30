# This is a single file test which shows all the required python code in one
# place. I kept this for reference, but I prefer the refactored code in
# logsetup which makes it more readable and re-usable.
import logging
from logging import StreamHandler
from logstash_formatter import LogstashFormatterV1
from logstash_async.handler import AsynchronousLogstashHandler
import sys
import os

# most of this is from the python logstash example:
# https://pypi.python.org/pypi/python-logstash

host = os.getenv('LOGSTASH_HOST', 'localhost')
port = int(os.getenv('LOGSTASH_PORT', 5959))

formatter = LogstashFormatterV1(fmt='{"extra": {"appname": "lstest"}}')

handler = AsynchronousLogstashHandler(host, port, database_path='logstash.db')
handler.setFormatter(formatter)

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(handler)
test_logger.addHandler(StreamHandler(stream=sys.stdout))


# this part is from SO:
# https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    test_logger.error("Uncaught exception (override handler)",
                      exc_info=(exc_type, exc_value, exc_traceback))


# don't forget to set the sys handler:
sys.excepthook = handle_exception


def main():
    try:
        test_logger.error('python-logstash: test logstash error message.')
        test_logger.info('python-logstash: test logstash info message.')
        test_logger.warning('python-logstash: test logstash warning message.')

        # add extra field to logstash message
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
        test_logger.info('python-logstash: test extra fields', extra=extra)
        x = extra['undefinedfield']
        test_logger.info(x)
    except Exception as e:
        test_logger.exception('exception raised')
    x = extra['undefinedfield']
    test_logger.info(x)


if __name__ == "__main__":
    main()
