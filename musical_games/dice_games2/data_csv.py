__author__ = 'Robbert Harms'
__date__ = '2024-04-11'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import csv
from abc import ABCMeta, abstractmethod
from importlib.abc import Traversable
from pathlib import Path
import re

from musical_games.dice_games2.base import Bar, BarCollection, SimpleBar, SimpleSynchronousBars, SimpleBarCollection, \
    SimpleMultiVoiceBar


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

    def __init__(self, staff_names: list[str]):
        """A simple CSV writer for bar collections.

        We should provide a staff name for any given staff in a synchronous bar. This stores each bar using the lilypond
        string.

        Args:
            staff_names: the names of the staffs. In the case of multi-voice staffs we will store
        """
        self._staff_names = staff_names

    def write_csv(self, bar_collection: BarCollection, csv_out: Path):
        with open(csv_out, 'w', newline='') as csvfile:
            bar_writer = csv.writer(csvfile, dialect='unix')

            bar_writer.writerow(['bar_index'] + self._staff_names)

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
                        bars.append(self._load_bar(bar_str))
                    synchronous_bars[int(row[0])] = SimpleSynchronousBars(dict(zip(staff_names, bars)))

        return SimpleBarCollection(synchronous_bars)

    @staticmethod
    def _load_bar(bar_str: str) -> Bar:
        """Load a Bar object from a CSV value string.

        This function will try to autodetect voices and load these as such.

        Args:
            bar_str: the CSV value to load.

        Returns:
            The loaded bar data.
        """
        voices = bar_str[3:-3].split('\\new Voice')

        if len(voices) > 1:
            voice_names_to_index = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4}
            voice_results = {}
            for voice_data in voices:
                match_groups = re.search(r"{\\voice([a-zA-Z]+) (.*)}", voice_data).groups()
                voice_results[voice_names_to_index[match_groups[0]]] = SimpleBar(match_groups[1])
            return SimpleMultiVoiceBar(voice_results)
        else:
            return SimpleBar(bar_str)

