__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from importlib import resources
import jinja2
from musical_games.dice_games.dice_game import load_dice_game

dice_games = [
    'cpe_bach_counterpoint',
    'kirnberger_menuet_trio',
    'kirnberger_polonaise',
    'mozart_waltz',
    'stadler_menuet_trio'
]


def load_inbuilt_dice_game(dice_game_name):
    """Load the indicated inbuilt dice game.

    Args:
        dice_game_name (str): one of the list of ``dice_games``

    Returns:
        musical_games.dice_games.dice_game.DiceGame: the dice game information
    """
    with resources.path(f'musical_games.data.dice_games.{dice_game_name}', 'config.yaml') as path:
        dice_game = load_dice_game(str(path))

    dice_game.typeset_env = create_jinja2_environment(
        jinja2.PackageLoader(f'musical_games.data.dice_games.{dice_game_name}', 'lilypond')
    )

    return dice_game


def create_jinja2_environment(loader):
    """Create a default jinja2 environment for typesetting compositions.

    Args:
        loader (jinja2.Loader): the loader for the data files.

    Returns:
        jinja2.Environment: the environment for typesetting a composition
    """
    return jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%-',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        lstrip_blocks=True,
        loader=loader)


