from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = '2024-04-11'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import csv
from abc import ABCMeta, abstractmethod
from importlib.abc import Traversable
from pathlib import Path

from frozendict import frozendict

from musical_games.dice_games.base import BarCollection, SimpleBar, SimpleBarCollection, BarAnnotation, int_bar_index, \
    str_staff_name, SimpleSynchronousBarSequence, SimpleSynchronousBar


class BarCollectionCSVWriter(metaclass=ABCMeta):
    """A CSV writer for a bar collection."""

    @abstractmethod
    def write_csv(self, bar_collection: BarCollection, csv_out: Path):
        """Write the given bar collection to a CSV file.

        Args:
            bar_collection: the collection of bars to write
            csv_out: the CSV output file
        """


class BarCollectionLoader(metaclass=ABCMeta):
    """Definition of a bar collection loader.

    Bar collection may be stored in different formats, implementing classes may specify these further.
    """

    @abstractmethod
    def load_data(self) -> BarCollection:
        """Load the bar collection.

        Returns:
            The loaded bar collection.
        """


class SimpleBarCollectionCSVWriter(BarCollectionCSVWriter):
    """A simple CSV writer for bar collections."""

    def write_csv(self, bar_collection: BarCollection, csv_out: Path):
        staff_names = bar_collection.get_staff_names()

        with open(csv_out, 'w', newline='') as csvfile:
            bar_writer = csv.writer(csvfile, dialect='unix')

            bar_writer.writerow(['bar_index', 'sequence_index'] + staff_names)

            for bar_index, synchronous_bar_sequence in bar_collection.get_synchronous_bar_sequences().items():
                sync_bars = synchronous_bar_sequence.get_synchronous_bars()
                for sequence_ind, sync_bar in enumerate(sync_bars):
                    row = [bar_index, sequence_ind] + [bar.lilypond_str for bar in sync_bar.get_bars()]
                    bar_writer.writerow(row)


class CSVBarCollectionLoader(BarCollectionLoader):

    def __init__(self,
                 bar_data_csv: Path | Traversable,
                 annotation_data_csv: Path | Traversable | None = None,
                 annotation_loader: AnnotationLoader | None = None):
        """Load a bar collection for a CSV file.

       When using this bar collection loader, bar's data are stored in CSV files, with for each synchronous bar,
       for each staff the lilypond score data. A separate file with annotations may additionally be loaded.
       This annotation file should have the same number of bars and staffs as the bar data, but contains a string
       of annotation data which can be loaded by the annotation loader.

       Args:
           bar_data_csv: path reference to the bar's data to load
           annotation_data_csv: reference to the annotation data to load
           annotation_loader: the factory method for the annotations's data.
       """
        self._bar_data_csv = bar_data_csv
        self._annotation_data_csv = annotation_data_csv
        self._annotation_loader = annotation_loader

    def load_data(self) -> BarCollection:
        annotations = None
        if self._annotation_data_csv is not None:
            annotations = self._load_annotations()

        bars_by_index_and_sequence = {}
        with (open(self._bar_data_csv, 'r', newline='') as csvfile):
            bar_reader = csv.reader(csvfile, dialect='unix')

            header = next(bar_reader)
            if header[1] == 'sequence_index':
                has_sequences = True
                staff_names = header[2:]
                first_data_column_ind = 2
            else:
                has_sequences = False
                staff_names = header[1:]
                first_data_column_ind = 1

            for row in bar_reader:
                sync_bars = {}
                for staff_ind, bar_str in enumerate(row[first_data_column_ind:]):
                    annotation = None
                    if annotations is not None:
                        annotation = annotations[int(row[0])][staff_names[staff_ind]]

                    sync_bars[staff_names[staff_ind]] = SimpleBar(bar_str, annotation=annotation)

                if has_sequences:
                    sequence_ind = row[1]
                else:
                    sequence_ind = 0

                sequence_dict = bars_by_index_and_sequence.setdefault(int(row[0]), {})
                sequence_dict[int(sequence_ind)] = SimpleSynchronousBar(frozendict(sync_bars))

        bar_collection = {}
        for bar_index, bar_sequences in bars_by_index_and_sequence.items():
            bar_collection[bar_index] = SimpleSynchronousBarSequence(
                tuple(dict(sorted(bar_sequences.items())).values()))

        return SimpleBarCollection(bar_collection)

    def _load_annotations(self) -> dict[int_bar_index, dict[str_staff_name, BarAnnotation]]:
        """Load the annotations for each bar of each staff."""
        annotations_data = {}

        with open(self._annotation_data_csv, 'r', newline='') as csvfile:
            annotation_reader = csv.reader(csvfile, dialect='unix')

            staff_names = None
            for row_ind, row in enumerate(annotation_reader):
                if row_ind == 0:
                    staff_names = row[1:]
                else:
                    annotations = []
                    for annotation_str in row[1:]:
                        annotations.append(self._annotation_loader.load_annotation(annotation_str))
                    annotations_data[int(row[0])] = dict(zip(staff_names, annotations))

        return annotations_data


class AnnotationLoader(metaclass=ABCMeta):
    """Factory class for annotation data.

    An instance of this class is needed when bar annotations need to be loaded by a BarCollectionLoader.
    """

    def load_annotation(self, input_data: str) -> BarAnnotation:
        """Load a bar annotation from input data.

        Args:
            input_data: a string of input data

        Returns:
            An instantiated bar annotation object.
        """
