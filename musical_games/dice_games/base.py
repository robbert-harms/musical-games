import numpy as np

__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class PieceInfo(object):

    def __init__(self, name, tract_info, key_signature, time_signature, tempo, **kwargs):
        """Information about one of the pieces in a composition.

        Args:
            name (str): the name of this piece
            tract_info (list of TractInfo): the information about the tracts
            key_signature (KeySignature): the key signature
            time_signature (TimeSignature): the time signature
            tempo (TempoIndication): the tempo indication
            **kwargs extra items added to this struct
        """
        self.name = name
        self.tract_info = tract_info
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo = tempo

        for key, value in kwargs.items():
            setattr(self, key, value)


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

    def count_unique_combinations(self, doubles):
        """Count the number of possible unique combinations over the columns.

        Doubles in the same column will reduce the total number of combinations.

        Args:
            doubles (list of list of int): the list of double positions

        Returns:
            int: the total number of unique combinations possible
        """
        columns = self.table.shape[1]

        total = 1

        for column_ind in range(columns):
            unique_counter = self._get_unique_in_row(self.table[:,column_ind], doubles)
            total *= unique_counter

        return total

    def _get_unique_in_row(self, row, doubles):
        #todo
        counter = 0
        for item in row:
            if all(item not in double_list[1:] for double_list in doubles):
                counter += 1
        print(counter)
        return counter