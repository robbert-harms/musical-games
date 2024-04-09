__author__ = 'Robbert Harms'
__date__ = '2024-04-07'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


class MissingDependencyError(Exception):
    """Raised when we are missing a crucial dependency for this library to fully function.

    For example, if we depend on a midi to wav converter but none can be found on the system,
    this exception may be raised.
    """
