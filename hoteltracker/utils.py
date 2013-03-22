import logging

def list_missing_args(required=(), provided=(), message=None):
    difference = set(required) - set(provided)

    if not message:
        return difference

    return message.format(args=', '.join(difference),
        s='s'[len(difference)==1:])

class TwitterHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        logging.Handler.__init__(self)

    def emit(self, record):
        # `record` is actually a `LogRecord` instance
        if getattr(record, 'tweet', False):
            pass