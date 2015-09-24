import csv
from musical_games.base import Bar
import numpy as np

__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class PieceInfo(object):

    def __init__(self, name, bar_collections, key_signature, time_signature, tempo):
        """Information about one of the pieces in a composition.

        Args:
            name: the name of this piece
        """
        self.name = name
        self.bar_collections = bar_collections
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo = tempo


class BarList(object):

    def __init__(self, name, bars):
        """Listing of all bars for a single tract.

        For example, use this for one BarList for the left hand of a piece and one for the right hand.

        Args:
            name (str): the name of this bar list
            bars (list of Bar): the list of bars in this barlist.
        """
        self.name = name
        self.bars = bars


class NumberedBar(Bar):

    def __init__(self, lilypond_code, bar_nmr, alternatives=None):
        super(NumberedBar, self).__init__(lilypond_code, alternatives=alternatives)
        self.bar_nmr = bar_nmr


class DiceTable(object):

    def __init__(self, name, table):
        """The dice table to use for playing a dice game.

        Args:
            name (str): the name of this dice table for printing purpose
            table (ndarray): numpy array containing the dice table
        """
        self.name = name
        self.table = table

    def get_random_indice(self, column):
        """Get the index of a random row in the dice table given the given column.

        Args:
            column (int): the column number we want to get a random row index from.

        Returns:
            int: the index to a measure for one specific column and a random row
        """
        return self.table[np.random.randint(self.table.shape[0]), column]

    def get_random_indices(self):
        """Get a random list of indices, one for each column.

        Returns:
            list: list of indices, one per column
        """
        return [self.get_random_indice(column) for column in range(self.table.shape[1])]

    def get_all_indices(self):
        """Get a sorted list of all the indices in this table.

        Returns:
            list: list of all sorted indices in this table.
        """
        return sorted(self.table.flatten())

    def column_split(self, column):
        """Split this dice table into two dicetables depending on the given column.

        We split at the given column. So if you have columns 1,2,3,4 and split on 3 you get 1,2 and 3,4.

        Returns:
            list of DiceTable: one per split
        """
        return DiceTable(self.name, self.table[:, 0:column]), DiceTable(self.name, self.table[:, column:])


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
                alternatives = Bar(row[2:])
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