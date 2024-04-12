from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Self, TypeAlias

import jinja2
import numpy as np
from numpy.random import RandomState


int_bar_index: TypeAlias = int
int_voice_index: TypeAlias = int
str_dice_table_name: TypeAlias = str
str_staff_name: TypeAlias = str


class DiceGame(metaclass=ABCMeta):

    @property
    @abstractmethod
    def author(self) -> str:
        """Get the name of the composer of this dice game.

        Returns:
            The name of the composer.
        """

    @property
    @abstractmethod
    def title(self) -> str:
        """Get the title of this dice game.

        Returns:
            The title of the dice game.
        """

    @abstractmethod
    def get_dice_tables(self) -> dict[str_dice_table_name, DiceTable]:
        """Get dice tables in this dice game.

        This should return the dice tables as a dictionary mapping an arbitrary name to a dice table. The names may be
        used by users of this class to refer to specific measures of a specific dice table. For instance in
        :meth:`compile_single_bar`.

        Returns:
            The available dice tables in this game.
        """

    @abstractmethod
    def get_all_duplicate_bars(self) -> dict[str_dice_table_name, list[set[int_bar_index]]]:
        """Get a list of all the duplicate bars for each dice table.

        For each dice table, this should scan the bars belonging to that dice table for duplicates. We return each
        set of duplicates as a set containing all the bar indices having duplicates.

        Returns:
            A list of duplicate bar sets by bar index for each dice table
        """

    @abstractmethod
    def count_unique_compositions(self, count_duplicates=False) -> int:
        """Count the number of unique compositions possible by this dice game.

        Args:
            count_duplicates (boolean): if set to False, we exclude all identical bars in a column of the dice matrix.

        Returns:
            The number of unique compositions
        """

    @abstractmethod
    def get_nmr_staffs_per_table(self) -> dict[str_dice_table_name, int]:
        """Get the number of staffs available per dice table.

        Returns:
            Per dice table, the number of staffs available in the measures table.
        """

    @abstractmethod
    def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
        """Get a random bar selection we may use to create a composition.

        Args:
            shuffle_staffs: if we want to shuffle the staffs within a dice table independently.
            seed: a seed for the random number generator.

        Returns:
            A bar selection object with the selected bars to form a composition.
        """

    @abstractmethod
    def bar_selection_to_bars(self, bar_selection: BarSelection) -> dict[str_dice_table_name, list[SynchronousBar]]:
        """Transform a bar selection (containing bar indices) to the actual selection of bars.

        The bar selection contains per dice table, and optionally per staff, the bar indices we want to use in a
        composition. This function should select from the collection of bars hold in this dice game the bars
        corresponding to the bar indices in the bar selection.

        Args:
            bar_selection: the selected bar indices contained in a bar selection

        Returns:
            For each dice table the bars to use as synchronous bars.
        """

    @abstractmethod
    def get_default_midi_settings(self) -> MidiSettings:
        """Get the default midi settings used when rendering a composition audio.

        Returns:
            The default midi settings used when rendering the audio of a composition.
        """

    @abstractmethod
    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        """Get an overview of all the bars as a lilypond score.

        Args:
            single_page: if we want to print the overview on a single large page without page breaks.

        Returns:
            A lilypond score with all the bars.
        """

    @abstractmethod
    def compile_single_bar(self, table_name: str_dice_table_name, bar_ind: int_bar_index) -> LilypondScore:
        """Get a lilypond score with only a single bar from one of the dice tables.

        Args:
            table_name: the specific dice table to use. Names should match those of the method :meth:`get_dice_tables`.
            bar_ind: the specific bar to lookup in the set of all bars. Should be an element of the referred table.

        Returns:
            A lilypond score for the single bar
        """

    @abstractmethod
    def compile_composition_score(self, bar_selection: BarSelection, comment: str | None = None) -> LilypondScore:
        """Compile a visual composition of this dice game using the selected bars.

        Args:
            bar_selection: the selection of bars for the composition
            comment: an optional comment for at the end of the composition

        Returns:
            A lilypond score meant to be rendered as a PDF.
        """

    @abstractmethod
    def compile_composition_audio(self, bar_selection: BarSelection,
                                  midi_settings: MidiSettings | None = None) -> LilypondScore:
        """Compile an auditive composition of this dice game using the selected bars.

        Args:
            bar_selection: the selection of bars for the composition
            midi_settings: the midi settings to use when typesetting the audio

        Returns:
            A lilypond score meant to be rendered as a midi
        """


class SimpleDiceGame(DiceGame, metaclass=ABCMeta):

    def __init__(self,
                 author: str,
                 title: str,
                 dice_tables: dict[str_dice_table_name: DiceTable],
                 bar_collections: dict[str_dice_table_name, BarCollection],
                 jinja2_environment: jinja2.Environment,
                 default_midi_settings: MidiSettings):
        """Implementation of a simple dice game covering most standard dice games functionality.

        Args:
            author: the author of the dice game
            title: the title of the dice game
            dice_tables: the dice tables indexed by table name
            bar_collections: the collection of bars per table
            jinja2_environment: the jinja2 environment we use for typesetting
            default_midi_settings: the default midi settings
        """
        self._author = author
        self._title = title
        self._dice_tables = dice_tables
        self._bar_collections = bar_collections
        self._jinja2_environment = jinja2_environment
        self._default_midi_settings = default_midi_settings

    @property
    def author(self) -> str:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    def get_dice_tables(self) -> dict[str_dice_table_name, DiceTable]:
        return self._dice_tables

    def get_all_duplicate_bars(self) -> dict[str_dice_table_name, list[set[int_bar_index]]]:
        table_duplicates = {}
        for table_name, dice_table in self._dice_tables.items():
            bars = self._bar_collections[table_name].get_synchronous_bars()

            bars_by_lilypond = {}
            for bar_ind, bar in bars.items():
                bar_data = tuple(b.lilypond_str for b in bar.get_staffs().values())
                bar_indices = bars_by_lilypond.setdefault(bar_data, set())
                bar_indices.add(bar_ind)

            table_duplicates[table_name] = [v for k, v in bars_by_lilypond.items() if len(v) > 1]
        return table_duplicates

    def count_unique_compositions(self, count_duplicates=False) -> int:
        def count_unique_bars(table_name: str, bar_indexes: list[int]):
            """Count the number of unique bars in the provided list of bar numbers."""
            bars_of_table = self._bar_collections[table_name]
            bars = [tuple(el.lilypond_str for el in bars_of_table.get_synchronous_bar(bar_index).get_bars())
                    for bar_index in bar_indexes]
            return len(set(bars))

        table_counts = []
        for table_name, table in self._dice_tables.items():
            if count_duplicates:
                table_counts.append(table.max_dice_value ** table.nmr_throws)
            else:
                table_counts.append(reduce(mul, [count_unique_bars(table_name, column)
                                                 for column in table.list_columns()]))
        return reduce(mul, table_counts)


    def get_nmr_staffs_per_table(self) -> dict[str_dice_table_name, int]:
        return {table_name: len(bar_collection.get_staff_names())
                for table_name, bar_collection in self._bar_collections.items()}

    def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
        choices = {}
        for table_name, dice_table in self._dice_tables.items():
            choices[table_name] = dice_table.get_random_selection(seed)
        return GroupedStaffsBarSelection(choices)

    def bar_selection_to_bars(self, bar_selection: BarSelection) -> dict[str_dice_table_name, list[SynchronousBar]]:
        composition_bars = {table_name: [] for table_name in self._dice_tables.keys()}

        for table_name in self._dice_tables.keys():
            for throw_ind in range(self._dice_tables[table_name].nmr_throws):
                bars_per_index = {}
                for staff_name in self._bar_collections[table_name].get_staff_names():
                    bar_ind = bar_selection.get_bar_index(table_name, throw_ind, staff_name)
                    bars_per_index[staff_name] = self._bar_collections[table_name].get_bar(staff_name, bar_ind)
                composition_bars[table_name].append(SimpleSynchronousBar(bars_per_index))
        return composition_bars

    def get_default_midi_settings(self) -> MidiSettings:
        return self._default_midi_settings

    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        template = self._jinja2_environment.get_template('bar_overview.ly')
        return SimpleLilypondScore(template.render(bar_collections=self._bar_collections,
                                                   render_settings={'single_page': single_page}))

    def compile_single_bar(self, table_name: str_dice_table_name, bar_ind: int_bar_index) -> LilypondScore:
        template = self._jinja2_environment.get_template('single_bar.ly')
        synchronous_bar = self._bar_collections[table_name].get_synchronous_bar(bar_ind)
        return SimpleLilypondScore(template.render(table_name=table_name, synchronous_bar=synchronous_bar))

    def compile_composition_score(self, bar_selection: BarSelection, comment: str | None = None) -> LilypondScore:
        template = self._jinja2_environment.get_template('composition_pdf.ly')
        composition_bars = self.bar_selection_to_bars(bar_selection)
        return SimpleLilypondScore(template.render(composition_bars=composition_bars,
                                                   render_settings={'comment': comment}))

    def compile_composition_audio(self, bar_selection: BarSelection,
                                  midi_settings: MidiSettings | None = None) -> LilypondScore:
        midi_settings = midi_settings or self.get_default_midi_settings()
        template = self._jinja2_environment.get_template('composition_midi.ly')
        composition_bars = self.bar_selection_to_bars(bar_selection)
        return SimpleLilypondScore(template.render(composition_bars=composition_bars, midi_settings=midi_settings))

    @staticmethod
    def _standard_jinja2_environment_options():
        """Get a set of standard jinja2 environment options you can use in your templates."""
        return dict(
            block_start_string=r'\BLOCK{',
            block_end_string='}',
            variable_start_string=r'\VAR{',
            variable_end_string='}',
            comment_start_string=r'\#{',
            comment_end_string='}',
            line_statement_prefix='%-',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            lstrip_blocks=True
        )


class Bar(metaclass=ABCMeta):
    """Representation of a single bar, of a single staff."""

    @property
    @abstractmethod
    def lilypond_str(self) -> str:
        """Get a representation of this bar as a lilypond string.

        Returns:
            A lilypond string of a single bar.
        """


class MultiVoiceBar(Bar, metaclass=ABCMeta):
    """Representation of a single bar with multiple voices."""

    @abstractmethod
    def get_voices(self) -> dict[int_voice_index, Bar]:
        """Get the voices stored in this multi-voice bar.

        Returns:
            Each voice should be returned as a separate bar object, indexed by their voice number.
        """


class SynchronousBar(metaclass=ABCMeta):
    """Representation of a list of bars played synchronously across staves.

    Suppose that a piece has a piano and a violin, then at each time point there are three bars being played, left and
    right hand piano and the violin. These synchronous bars are connected in this class. For clarity, the different
    bars should be stored in a dictionary with their staff name as key.
    """
    @abstractmethod
    def get_staff_names(self) -> list[str_staff_name]:
        """Get the names of the staffs stored in this synchronous bar.

        Returns:
            The names of the staffs
        """

    @abstractmethod
    def get_staffs(self) -> dict[str, Bar]:
        """Get the collection of bars being played at the same time.

        Returns:
            The bars across staves.
        """

    @abstractmethod
    def get_bar(self, staff_name: str_staff_name) -> Bar:
        """Get a single bar from a single staff.

        Args:
            staff_name: the name of the staff for which you want the bar.

        Returns:
            The bar of that staff.
        """

    @abstractmethod
    def get_bars(self) -> list[Bar]:
        """Get the bars in a list.

        Returns:
            The list of bars, in the order defined by the dictionary.
        """


class BarCollection(metaclass=ABCMeta):
    """Collection of synchronous bars for a single compositional piece.

    The bars are expected to be stored in a dictionary mapping bar indices to bars.
    """

    @abstractmethod
    def get_synchronous_bars(self) -> dict[int_bar_index, SynchronousBar]:
        """Get the collection of all synchronous bars.

        Returns:
            All synchronous bars indexed by their bar index.
        """

    @abstractmethod
    def get_synchronous_bar(self, bar_index: int_bar_index) -> SynchronousBar:
        """Get a synchronous bar at the specified bar index.

        Args:
            bar_index: the index of the bar to retrieve.

        Returns:
            The synchronous bar at that bar index.
        """

    @abstractmethod
    def get_staff_names(self) -> list[str_staff_name]:
        """Get the names of the staffs stored in the synchronous bars.

        Returns:
            The names of the staffs.
        """

    @abstractmethod
    def get_bars(self, staff_name: str_staff_name) -> dict[int_bar_index, Bar]:
        """Get the collection of bars of a single staff.

        Args:
            staff_name: the name of the staff for which we want to return the bars.

        Returns:
            All bars of a single staff indexed by their bar index..
        """

    @abstractmethod
    def get_bar(self, staff_name: str_staff_name, bar_index: int_bar_index) -> Bar:
        """Get a single bar from a specific staff.

        Args:
            staff_name: the name of the staff
            bar_index: the index of the bar

        Returns:
            The specific bar in the given staff and bar index locations.
        """


@dataclass(frozen=True, slots=True)
class SimpleBar(Bar):
    """Dataclass representation of a single bar, of a single staff.

    Args:
        lilypond_str: the lilypond string representation of this bar
    """
    lilypond_str: str


@dataclass(frozen=True, slots=True)
class SimpleMultiVoiceBar(MultiVoiceBar):
    """Representation of a single bar with multiple voices.

    Since in a piece there may be multiple voices which we may want to connect, we index the voices in this
    class by a voice index number. As such, if, for example, voice 3 drops out for a section, the indices
    stay constant.

    Args:
        A mapping of voice number to a bar.
    """
    voices: dict[int_voice_index, Bar]

    @property
    def lilypond_str(self) -> str:
        voices_index_to_name = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four'}
        voice_strings = []
        for voice_ind, bar in self.voices.items():
            voice_strings.append("{\\voice" + voices_index_to_name[voice_ind] + ' ' + bar.lilypond_str + '}')
        return '{<<' + ' \\new Voice '.join(voice_strings) + '>>}'

    def get_voices(self) -> dict[int_voice_index, Bar]:
        return self.voices


@dataclass(frozen=True, slots=True)
class SimpleSynchronousBar(SynchronousBar):
    """Representation of a bar across staffs.

    Args:
        bars: the bars per staff.
    """
    bars: dict[str_staff_name, Bar]

    def get_staff_names(self) -> list[str_staff_name]:
        return list(self.bars.keys())

    def get_staffs(self) -> dict[str_staff_name, Bar]:
        return self.bars

    def get_bar(self, staff_name: str_staff_name) -> Bar:
        return self.bars[staff_name]

    def get_bars(self) -> list[Bar]:
        return list(self.bars.values())


@dataclass(frozen=True, slots=True)
class SimpleBarCollection(BarCollection):
    """Representation of a collection of bars contained in a dictionary.

    The bars are stored in a multi-level dictionary, combined into synchronous bars when asked. Furthermore, the bars
    are stored in a dictionary such that we can store the bars with their dice table label instead of a numerical index.

    Args:
        bar_collection: the collection of synchronous bars indexed by their bar index and staff name.
    """
    bar_collection: dict[int_bar_index, dict[str_staff_name, Bar]]

    def get_synchronous_bars(self) -> dict[int_bar_index, SynchronousBar]:
        return {bar_index: SimpleSynchronousBar(bars) for bar_index, bars in self.bar_collection.items()}

    def get_synchronous_bar(self, bar_index: int_bar_index) -> SynchronousBar:
        return SimpleSynchronousBar(self.bar_collection[bar_index])

    def get_staff_names(self) -> list[str_staff_name]:
        return list(self.bar_collection[1].keys())

    def get_bars(self, staff_name: str_staff_name) -> dict[int_bar_index, Bar]:
        return {bar_index: bars[staff_name] for bar_index, bars in self.bar_collection.items()}

    def get_bar(self, staff_name: str_staff_name, bar_index: int_bar_index) -> Bar:
        return self.bar_collection[bar_index][staff_name]


class DiceTable(metaclass=ABCMeta):
    """Representation of a dice table used in playing the dice games.

    This assumes all entries in the dice game tables are integers mapping to a bars in the bar table.
    """

    @property
    @abstractmethod
    def nmr_dices(self) -> int:
        """Get the number of dices this table needs."""

    @property
    @abstractmethod
    def max_dice_value(self) -> int:
        """Get the maximum dice value needed to select row from this dice table."""

    @property
    @abstractmethod
    def nmr_throws(self) -> int:
        """Get the maximum number of throws needed to select all the columns from this dice table."""

    @abstractmethod
    def list_rows(self) -> list[list[int]]:
        """Get a list with the list of row values"""

    @abstractmethod
    def list_columns(self) -> list[list[int]]:
        """Get a list with the list of column values"""

    @abstractmethod
    def get_column(self, column_ind: int) -> list[int]:
        """Get the column of the dice table at the indicated index.

        Args:
            column_ind: the index of the column (0 based)

        Returns:
            The dice game labels in the indicated column
        """

    @abstractmethod
    def get_row(self, row_ind: int) -> list[int]:
        """Get the row of the dice table at the indicated index.

        Args:
            row_ind: the index of the row (0 based)

        Returns:
            The dice game labels in the indicated row
        """


@dataclass(slots=True, frozen=True)
class SimpleDiceTable(DiceTable):
    """Implementation of a dice table using a numpy array."""
    table: np.ndarray

    @property
    def nmr_dices(self) -> int:
        return self.max_dice_value % 2

    @property
    def max_dice_value(self) -> int:
        return self.table.shape[0]

    @property
    def nmr_throws(self) -> int:
        return self.table.shape[1]

    def list_rows(self) -> list[list[int]]:
        return self.table.tolist()

    def list_columns(self) -> list[list[int]]:
        return self.table.T.tolist()

    def get_column(self, column_ind: int) -> list[int]:
        return self.table[:, column_ind].tolist()

    def get_row(self, row_ind: int) -> list[int]:
        return self.table[row_ind, :].tolist()

    def get_random_selection(self, seed: int = None) -> list[int]:
        """Get a random selection of bar numbers

        Returns:
            A list of random bar numbers from the table
        """
        prng = RandomState(seed)
        dice_throws = prng.randint(0, self.table.shape[0], self.table.shape[1])
        return self.table[dice_throws, range(self.table.shape[1])].tolist()


class LilypondScore(metaclass=ABCMeta):
    """Representation of a lilypond score."""

    @abstractmethod
    def get_score(self) -> str:
        """Get the score as a string.

        Returns:
            A completely compiles version of the score as a string.
        """

    @abstractmethod
    def to_file(self, out_file: Path):
        """Write the score to a file.

        Args:
            out_file: the file to write the score to.
        """


@dataclass(slots=True, frozen=True)
class SimpleLilypondScore(LilypondScore):
    """Implements a lilypond score from a precompiled score string.

    Args:
        score_str: the score as a single string.
    """
    score_str: str

    def get_score(self) -> str:
        return self.score_str

    def to_file(self, out_file: Path):
        out_file.parent.mkdir(parents=True, exist_ok=True)

        with open(out_file, 'w') as f:
            f.write(self.score_str)


class BarSelection(metaclass=ABCMeta):
    """Representation of a selection of bars chosen to compile into a dice game composition.

    This abstracts the notion of throwing the dice for a musical composition. We allow shuffling staffs within a dice
    table by selecting bar indices by table key and staff name.
    """

    @abstractmethod
    def get_bar_index(self,
                      table_name: str_dice_table_name,
                      throw_ind: int,
                      staff_name: str_staff_name | None = None) -> int_bar_index:
        """Get the bar index for a specific dice table, a specified throw index and optionally a specific staff.

        Args:
            table_name: the name of the dice table we have indices for
            throw_ind: the index of the dice throw
            staff_name: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The selected bar for this dice table, dice throw and staff.
        """

    @abstractmethod
    def get_bar_indices(self,
                        table_name: str_dice_table_name,
                        staff_name: str_staff_name | None = None) -> list[int_bar_index]:
        """Get the bar indices chosen for the specific dice table and staff (within that dice table).

        For a given table, this may either return the same bar indices for each staff, or a different list per staff.

        Args:
            table_name: the name of the dice table we have indices for
            staff_name: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The selected bar for this dice table, dice throw and staff.
        """


@dataclass(slots=True, frozen=True)
class GroupedStaffsBarSelection(BarSelection):
    """Bar selection where we select the same bar indices for each staff of a dice table.

    Args:
        bar_indices: for each table key, the list of bars we want to select in the composition.
    """
    bar_indices: dict[str_dice_table_name, list[int_bar_index]]

    def get_bar_index(self,
                      table_name: str_dice_table_name,
                      throw_ind: int,
                      staff_name: str_staff_name | None = None) -> int_bar_index:
        return self.bar_indices[table_name][throw_ind]

    def get_bar_indices(self,
                        table_name: str_dice_table_name,
                        staff_name: str_staff_name | None = None) -> list[int_bar_index]:
        return self.bar_indices[table_name]


@dataclass(slots=True, frozen=True)
class PerStaffsBarSelection(BarSelection):
    """Bar selection where we may select different bar indices for each staff of a dice table.

    Args:
        bar_indices: for each table key, and for each staff, the list of bars we want to select in the composition.
    """
    bar_indices: dict[str_dice_table_name, dict[str_staff_name, list[int_bar_index]]]

    def get_bar_index(self,
                      table_name: str_dice_table_name,
                      throw_ind: int,
                      staff_name: str_staff_name | None = None) -> int_bar_index:
        return self.bar_indices[table_name][staff_name][throw_ind]

    def get_bar_indices(self,
                        table_name: str_dice_table_name,
                        staff_name: str_staff_name | None = None) -> list[int_bar_index]:
        return self.bar_indices[table_name][staff_name]


class MidiSettings(metaclass=ABCMeta):

    @abstractmethod
    def get_midi_instrument(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> str:
        """Get the midi instrument to use for rendering the specific table and specific staff.

        Args:
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            The instrument name as a midi instrument name
        """

    @abstractmethod
    def get_min_volume(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> float:
        """Get the minimum volume to use for rendering the specific table and specific staff.

        Args:
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            The minimum volume to use.
        """

    @abstractmethod
    def get_max_volume(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> float:
        """Get the maximum volume to use for rendering the specific table and specific staff.

        Args:
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            The maximum volume to use.
        """

    @abstractmethod
    def with_updated_instrument(self, midi_instrument: str, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        """Get a version of this midi setting but with a different instrument for the given dice table and staff.

        Args:
            midi_instrument: the new instrument name to insert
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_min_volume(self, min_volume: float, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        """Get a version of this midi setting but with a different minimum volume for the given dice table and staff.

        Args:
            min_volume: the new minimum volume
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_max_volume(self, max_volume: float, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        """Get a version of this midi setting but with a different maximum volume for the given dice table and staff.

        Args:
            max_volume: the new maximum volume
            table_name: the specific table
            staff_name: the specific staff

        Returns:
            A new instance of this midi settings.
        """


@dataclass(frozen=True, slots=True)
class SimpleMidiSettings(MidiSettings):
    """Simple lookup implementation of the midi settings.

    Args:
        midi_instruments: the instruments to use, indexed by table key and staff name
        min_volumes: the minimum volumes to use, indexed by table key and staff name
        max_volumes: the maximum volumes to use, indexed by table key and staff name
    """
    midi_instruments: dict[str_dice_table_name, dict[str_staff_name, str]]
    min_volumes: dict[str_dice_table_name, dict[str_staff_name, float]]
    max_volumes: dict[str_dice_table_name, dict[str_staff_name, float]]

    def get_midi_instrument(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> str:
        return self.midi_instruments[table_name][staff_name]

    def get_min_volume(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> float:
        return self.min_volumes[table_name][staff_name]

    def get_max_volume(self, table_name: str_dice_table_name, staff_name: str_staff_name) -> float:
        return self.max_volumes[table_name][staff_name]

    def with_updated_instrument(self, midi_instrument: str, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        updated_dict = self.midi_instruments | {table_name: (self.midi_instruments[table_name]
                                                             | {staff_name: midi_instrument})}
        return type(self)(updated_dict, self.min_volumes, self.max_volumes)

    def with_updated_min_volume(self, min_volume: float, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        updated_dict = self.min_volumes | {table_name: (self.min_volumes[table_name] | {staff_name: min_volume})}
        return type(self)(self.midi_instruments, updated_dict, self.max_volumes)

    def with_updated_max_volume(self, max_volume: float, table_name: str_dice_table_name,
                                staff_name: str_staff_name) -> Self:
        updated_dict = self.max_volumes | {table_name: (self.max_volumes[table_name] | {staff_name: max_volume})}
        return type(self)(self.midi_instruments, self.min_volumes, updated_dict)
