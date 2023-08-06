def list_args_to_comma_separated(func):
    """Return function that converts list input arguments to comma-separated strings"""

    def input_args(*args, **kwargs):
        for v in kwargs:
            print(v)
            # check in **kwargs for lists and convert to comma-separated string
            if isinstance(kwargs[v], list): kwargs[v] = ','.join(kwargs[v])
            if isinstance(kwargs[v], bool):
                print(kwargs[v], 'bool')
                print('as txt:', str(kwargs[v]))
        # check in *args for lists and convert to comma-separated string
        args = [','.join(v) if isinstance(v, list) else v for v in args]
        return func(*args, **kwargs)

    return input_args


def get_comma_separated_values(values):
    """Return the values as a comma-separated string"""

    # Make sure values is a list or tuple
    if not isinstance(values, list) and not isinstance(values, tuple):
        values = [values]
    return ','.join(values)
