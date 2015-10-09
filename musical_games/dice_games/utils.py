import csv
import numpy as np
from musical_games.base import Bar
from musical_games.dice_games.base import NumberedBar

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def load_bars_from_file(filename):
    """Load bars from a given file.

    The file is supposed to be a CSV file with as first column the list of positions this bar appears in
    and the second column the lilypond code for that measure. The third and further columns can be alternatives
    for that measure.

    Args:
        filename (str): the name of the file we will load.
    """
    bar_dict = {}

    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row) > 2:
                alternatives = [Bar(r) for r in row[2:]]
            else:
                alternatives = None

            if ',' in row[0]:
                doubles = row[0].split(',')

                for position in doubles:
                    bar_dict.update({int(position): NumberedBar(row[1], position, alternatives)})
            else:
                bar_dict.update({int(row[0]): NumberedBar(row[1], row[0], alternatives)})

    positions = sorted(list(bar_dict.keys()))
    return [bar_dict[ind] for ind in positions]


def load_dice_table(filename):
    """Load one of the dicetables from CSV format.

    Args:
        filename (str): the filename of the dice table
    """
    return np.genfromtxt(filename, dtype=np.int32, delimiter=',')