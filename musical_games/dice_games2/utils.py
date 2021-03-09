__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


from dataclasses import MISSING


def get_default_value(field):
    """Resolve the default value of a dataclass field.

    This first looks if ``default`` is defined, next it tries to call the function ``default_factory``, else it
    returns None.

    Args:
        field (dataclass.field): one field of a class with @dataclass decorator

    Returns:
        Any: the default field object.
    """
    if hasattr(field, 'default') and field.default is not MISSING:
        return field.default
    elif hasattr(field, 'default_factory') and field.default_factory is not MISSING:
        return field.default_factory()
    return None
