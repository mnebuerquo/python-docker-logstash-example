# This file shows how to set up logging in a non-flask python script.
import sys
from logsetup import logstash_init

logger = logstash_init('testapp', {"extra_string": "This is a test"})


def main():
    try:
        logger.error('python-logstash: test logstash error message.')
        logger.info('python-logstash: test logstash info message.')
        logger.warning('python-logstash: test logstash warning message.')

        # add extra field to logstash message
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
        logger.info('python-logstash: test extra fields', extra=extra)
        x = extra['undefinedfield']
        logger.info(x)
    except Exception as e:
        logger.exception('exception raised')
    finally:
        print("finally")
    x = extra['undefinedfield']
    logger.info(x)


if __name__ == "__main__":
    main()
