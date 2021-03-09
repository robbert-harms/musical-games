__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from typing import Tuple

import dacite
from ruamel.yaml import YAML
from musical_games.dice_games2.dice_game_nodes import Composition


def read_config_file(fname):
    """Load the data from the provided configuration file and return an Composition object.

    Args:
        fname (str): the filename of the composition config file to load

    Returns:
        musical_games.dice_games.dice_game_nodes.Composition: the loaded composition
    """
    with open(fname, 'r', encoding='utf-8') as f:
        return read_composition_string(f.read())


def read_composition_string(yaml_str):
    """Load the data from the provided yaml formatted string and return a loaded Composition object

    Args:
        yaml_str (str): an yaml formatted string to load

    Returns:
        musical_games.dice_games.dice_game_nodes.Composition: the loaded composition
    """
    yaml = YAML(typ='safe')
    data = yaml.load(yaml_str)
    return dacite.from_dict(Composition, data, config=dacite.Config(
        type_hooks={
            Tuple[int, int]: tuple,
            Tuple[str, str]: tuple
        }))
