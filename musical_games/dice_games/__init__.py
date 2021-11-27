__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from importlib import resources
import jinja2
from musical_games.dice_games.dice_game import DiceGame
from musical_games.dice_games.lilypond import LilypondDiceGameTypesetter

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
        DiceGame: the dice game information
    """
    with resources.path(f'musical_games.data.dice_games.{dice_game_name}', 'config.yaml') as path:
        return DiceGame.from_file(str(path))


def load_inbuilt_dice_game_typesetter(dice_game, dice_game_name):
    """Load the Lilypond renderer for the indicated dice game.

    Args:
        dice_game (DiceGame): the loaded dice game.
        dice_game_name (str): one of the list of ``dice_games``

    Returns:
        LilypondDiceGameTypesetter: the dice game renderer
    """
    return LilypondDiceGameTypesetter(
        dice_game,
        jinja2.PackageLoader(f'musical_games.data.dice_games.{dice_game_name}', 'lilypond')
    )
