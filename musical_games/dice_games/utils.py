import csv
import collections
import numpy as np
from musical_games.base import Bar
from musical_games.dice_games.base import Bars, DiceTable

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

    Returns:
        Bars: the bars object holding the list of Bar objects
    """
    bar_dict = {}

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row) > 2:
                alternatives = [Bar(r) for r in row[2:]]
            else:
                alternatives = None

            if ',' in row[0]:
                doubles = list(map(int, row[0].split(',')))

                for position in doubles:
                    bar_dict.update({position: Bar(row[1], alternatives)})
            else:
                bar_dict.update({int(row[0]): Bar(row[1], alternatives)})

    return Bars(list(bar_dict[k] for k in sorted(bar_dict.keys())))


def load_dice_table(filename):
    """Load one of the dicetables from CSV format.

    Args:
        filename (str): the filename of the dice table (in CSV format)

    Returns:
        DiceTable: the dice table with the data loaded from the given file
    """
    return DiceTable(np.genfromtxt(filename, dtype=np.int32, delimiter=','))


def find_duplicate_bars(bars_list):
    """Find the bars that are double in the given bar lists

    This will find the positions in which all bars on a given position have the same data.
    Suppose you have two Bars with the following items:
        ['a', 'b', 'a', 'e']
        ['g', 'c', 'g', 'c']

    This function will then return [[0, 2]] indicating that it has found one set of doubles and
    that set of doubles occurs at positions zero and two.

    Positions 1 and 3 are not doubles since they are not equal over all Bars.

    Args:
        bars_list (list of Bars): the list of Bars from which we want to find the overall doubles

    Returns:
        list of list of int: the tuples with information about the doubles.
            This returns a list holding lists with per similar measures the positions of that measure. The indices
            returned are in Dice Table space (that is 1-based).
    """
    positions = range(bars_list[0].length())

    bar_pairs = []
    for position in positions:
        bar_pairs.append(hash(tuple(bars.get_at_index(position) for bars in bars_list)))

    def duplicates(lst):
        cnt = collections.Counter(lst)
        return [key for key, val in cnt.items() if val > 1]

    def duplicates_indices(lst):
        dup = duplicates(lst)
        ind = collections.defaultdict(list)
        for i, v in enumerate(lst):
            if v in dup:
                ind[v].append(i)
        return ind

    dups = duplicates_indices(bar_pairs).values()
    return [list(map(lambda v: v + 1, dup_list)) for dup_list in dups]
