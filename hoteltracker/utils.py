def list_missing_args(required=(), provided=(), message=None):
    difference = set(required) - set(provided)

    if not message:
        return difference

    return message.format(args=', '.join(difference),
        s='s'[len(difference)==1:])