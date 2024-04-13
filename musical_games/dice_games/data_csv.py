__author__ = 'Robbert Harms'
__date__ = '2024-04-11'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import csv
from abc import ABCMeta, abstractmethod
from importlib.abc import Traversable
from pathlib import Path

from musical_games.dice_games.base import BarCollection, SimpleBar, SimpleBarCollection


class BarCollectionCSVWriter(metaclass=ABCMeta):
    """A CSV writer for a bar collection."""

    @abstractmethod
    def write_csv(self, bar_collection: BarCollection, csv_out: Path):
        """Write the given bar collection to a CSV file.

        Args:
            bar_collection: the collection of bars to write
            csv_out: the CSV output file
        """


class BarCollectionCSVReader(metaclass=ABCMeta):
    """A CSV reader for a bar collection."""

    @abstractmethod
    def read_csv(self, csv_in: Path | Traversable) -> BarCollection:
        """Read a bar collection from a CSV.

        Args:
            csv_in: the CSV file to read

        Returns:
            The bar collection loaded from the indicated CSv.
        """


class SimpleBarCollectionCSVWriter(BarCollectionCSVWriter):
    """A simple CSV writer for bar collections."""

    def write_csv(self, bar_collection: BarCollection, csv_out: Path):
        staff_names = bar_collection.get_staff_names()

        with open(csv_out, 'w', newline='') as csvfile:
            bar_writer = csv.writer(csvfile, dialect='unix')

            bar_writer.writerow(['bar_index'] + staff_names)

            for bar_index, synchronous_bars in bar_collection.get_synchronous_bars().items():
                row = [bar_index] + [bar.lilypond_str for bar in synchronous_bars.get_bars()]
                bar_writer.writerow(row)


class SimpleBarCollectionCSVReader(BarCollectionCSVReader):
    """A simple CSV reader for bar collections.

    We try to automatically detect multi-voice bars, by looking for '<<' and '>>'.
    """

    def read_csv(self, csv_in: Path | Traversable) -> BarCollection:
        synchronous_bars = {}

        with open(csv_in, 'r', newline='') as csvfile:
            bar_reader = csv.reader(csvfile, dialect='unix')

            staff_names = None
            for row_ind, row in enumerate(bar_reader):
                if row_ind == 0:
                    staff_names = row[1:]
                else:
                    bars = []
                    for bar_str in row[1:]:
                        bars.append(SimpleBar(bar_str))
                    synchronous_bars[int(row[0])] = dict(zip(staff_names, bars))

        return SimpleBarCollection(synchronous_bars)
