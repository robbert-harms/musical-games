__author__ = 'Robbert Harms'
__date__ = '2015-01-01'
__email__ = 'robbert@xkls.nl'
__license__ = "LGPL v3"
__maintainer__ = "Robbert Harms"

VERSION = '0.3.14'
VERSION_STATUS = ''

_items = VERSION.split('-')
VERSION_NUMBER_PARTS = tuple(int(i) for i in _items[0].split('.'))
if len(_items) > 1:
    VERSION_STATUS = _items[1]
__version__ = VERSION
