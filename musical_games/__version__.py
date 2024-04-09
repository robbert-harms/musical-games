__author__ = 'Robbert Harms'
__date__ = '2015-01-01'
__email__ = 'robbert@xkls.nl'
__license__ = "LGPL v3"
__maintainer__ = "Robbert Harms"


from importlib import metadata
from importlib.metadata import PackageNotFoundError
from pathlib import Path

import tomllib

try:
    __version__ = metadata.version('musical_games')
except PackageNotFoundError:
    with open(Path(__file__).parent.parent / 'pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
        __version__ = pyproject['project']['version']
