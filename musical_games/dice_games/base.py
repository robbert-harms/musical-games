import numpy as np

from musical_games.base import Bar

__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class PieceInfo(object):

    def __init__(self, name, tract_info, key_signature, time_signature, tempo):
        """Information about one of the pieces in a composition.

        Args:
            name: the name of this piece
        """
        self.name = name
        self.tract_info = tract_info
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo = tempo


class TractInfo(object):

    def __init__(self, name, clef, bars):
        """Information about a single tract.

        For example, you can have two of these, one for the left hand of a piece and one for the right hand
        (in the case of a piano).

        Args:
            name (str): the name of this bar list
            clef (str): lilypond clef notation string. Like 'treble' or 'bass'
            bars (list of Bar): the list of bars in this barlist.
        """
        self.name = name
        self.clef = clef
        self.bars = bars


class NumberedBar(Bar):

    def __init__(self, lilypond_code, bar_nmr, alternatives=None):
        """Subclass of Bar, adds the bar number to the bar information."""
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

    def random_index(self, column):
        """Get the index of a random row in the dice table given the given column.

        Args:
            column (int): the column number we want to get a random row index from.

        Returns:
            int: the index to a measure for one specific column and a random row
        """
        return self.table[np.random.randint(self.table.shape[0]), column]

    def random_indices(self):
        """Get a random list of indices, one for each column.

        Returns:
            list: list of indices, one per column
        """
        return [self.random_index(column) for column in range(self.table.shape[1])]

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