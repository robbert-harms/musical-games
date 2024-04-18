__author__ = 'Robbert Harms'
__date__ = '2024-04-18'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.base import DiceGame
from musical_games.dice_games.dice_games import CPEBachCounterpoint
from musical_games.utils import auto_convert_lilypond_file


def generate_statics(dice_game: DiceGame, out_dir: Path):
    """For a given dice game, generate the static output files.

    The static output files are the bars overview pdf, and the images for each dice table element (which may contain
    multiple bars depending on the dice table).

    The output directory is filled with the following directories and files:

    - bars_overview.pdf: the overview of all the bars
    - dice_table_elements/<table_name>/r<row_index>_c<column_index>.png: for each dice table and for each dice table
        element an image with the generated dice table element.

    Args:
          dice_game: the dice game from which we want to generate the statics
          out_dir: the output directory for the files.
    """
    dice_game.compile_bars_overview(single_page=False).to_file(out_dir / 'bars_overview.ly')
    auto_convert_lilypond_file(out_dir / 'bars_overview.ly', pdf=True, png=False)

    for table_name, dice_table in dice_game.get_dice_tables().items():
        for dice_table_element in dice_table.get_elements():
            ly_out = (out_dir / f'{table_name}_bars' /
                      f'r{dice_table_element.row_ind}_c{dice_table_element.column_ind}.ly')
            dice_game.compile_single_dice_table_element(table_name, dice_table_element).to_file(ly_out)
            auto_convert_lilypond_file(ly_out, pdf=False, png=True, trim_png=True)

generate_statics(CPEBachCounterpoint(), Path('/tmp/overview'))
