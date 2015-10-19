import csv
import collections
import numpy as np
from musical_games.base import Bar

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
        dict: as key the indices, as values the Bar objects
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
                doubles = list(map(int, row[0].split(',')))

                for position in doubles:
                    bar_dict.update({position: Bar(row[1], alternatives)})
            else:
                bar_dict.update({int(row[0]): Bar(row[1], alternatives)})

    return bar_dict


def load_dice_table(filename):
    """Load one of the dicetables from CSV format.

    Args:
        filename (str): the filename of the dice table
    """
    return np.genfromtxt(filename, dtype=np.int32, delimiter=',')


def find_double_bars(bar_dict_lists):
    """Find the bars that are double in the given bar lists

    This will find the positions in which all bars on a given position have the same data.
    Suppose you have two bar lists with the following items:
        ['a', 'b', 'a', 'b']
        ['g', 'c', 'g', 'c']

    This function will then return [[0, 2]] indicating that it has found one set of doubles at positions zero and two.

    Args:
        list of bar dicts: the bar dicts we use to find the doubles

    Returns:
        tuple of tuples: the tuples with information about the doubles
    """
    positions = bar_dict_lists[0].keys()
    bar_pairs = []
    for position in positions:
        bar_pairs.append(hash(tuple(bdl[position] for bdl in bar_dict_lists)))

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