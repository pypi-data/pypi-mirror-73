import warnings
from typing import List

from decorator import decorator


def show_message(error_msg: str, warning_instead_of_error: bool) -> None:
    if warning_instead_of_error:
        warnings.warn(error_msg)
    else:
        raise TypeError(error_msg)


def manage_error_in_parameter_types(checks: List[int], names: tuple, args: tuple, hints: dict, warning_instead_of_error: bool) -> None:
    warning_text = ["Parameter's type mismatch"]
    for check, name, arg in zip(checks, names, args):
        if check == 1:
            warning_text.append("Parameter's name: {}, expected: {} but got: {}".format(name, hints[name], type(arg)))

    error_msg = "\n\t".join(warning_text)
    show_message(error_msg, warning_instead_of_error)


@decorator
def enforce_type_hints(f, disable: bool = False, warning_instead_of_error: bool = False, *args, **kw):
    if disable:
        return f

    hints = f.__annotations__
    names = f.__code__.co_varnames

    # Check the types of the parameters
    checks = [0 if isinstance(arg, hints[name]) else 1 for name, arg in zip(names, args)]

    if 1 in checks:
        manage_error_in_parameter_types(checks, names, args, hints, warning_instead_of_error)

    result = f(*args, **kw)

    # Check the type of the returned object
    if 'return' in hints and not isinstance(result, hints['return']):
        error_msg = "Return type mismatch, expected: {} but got: {}".format(hints['return'], type(result))
        show_message(error_msg, warning_instead_of_error)

    return result
