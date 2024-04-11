from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Self, TypeAlias

import numpy as np
from numpy.random import RandomState


int_bar_index: TypeAlias = int
str_dice_table_key: TypeAlias = str
int_voice_index: TypeAlias = int
int_staff_index: TypeAlias = int


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
    def get_dice_tables(self) -> dict[str_dice_table_key, DiceTable]:
        """Get dice tables in this dice game.

        This should return the dice tables as a dictionary mapping an arbitrary key to a dice table. The keys may be
        used by users of this class to refer to specific measures of a specific dice table. For instance in
        :meth:`compile_single_bar`.

        Returns:
            The available dice tables in this game.
        """

    @abstractmethod
    def get_all_duplicate_bars(self, table_key: str_dice_table_key) -> list[set[int_bar_index]]:
        """Get a list of all the duplicate bars in a given dice table.

        For a given dice table, this should scan the bars belonging to that dice table for duplicates. We return each
        set of duplicates as a set containing all the bar indices having duplicates.

        Args:
            table_key: the key of the dice table we want to search for duplicates.

        Returns:
            A list of duplicate bar sets by bar index.
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
    def get_nmr_staffs_per_table(self) -> dict[str, int]:
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
    def compile_single_bar(self, table_key: str_dice_table_key, bar_ind: int_bar_index) -> LilypondScore:
        """Get a lilypond score with only a single bar from one of the dice tables.

        Args:
            table_key: the specific dice table to use. Keys should match those of the method :meth:`get_dice_tables`.
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


class SynchronousBars(metaclass=ABCMeta):
    """Representation of a list of bars played synchronously across staves.

    Suppose that a piece has a piano and a violin, then at each time point there are three bars being played, left and
    right hand piano and the violin. These synchronous bars are connected in this class.
    """

    @abstractmethod
    def get_bars(self) -> tuple[Bar, ...]:
        """Get the collection of bars being played at the same time.

        Returns:
            The bars across staves.
        """

    @abstractmethod
    def get_bar(self, staff_ind: int_staff_index) -> Bar:
        """Get a single bar from a single staff.

        Args:
            staff_ind: the index of the staff for which you want the bar.

        Returns:
            The bar of that staff.
        """


class BarCollection(metaclass=ABCMeta):
    """Collection of synchronous bars for a single compositional piece.

    The bars are expected to be stored in a dictionary mapping dice table labels (bar indices) to bars.
    """

    @abstractmethod
    def get_synchronous_bars(self) -> dict[int_bar_index, SynchronousBars]:
        """Get the collection of all synchronous bars.

        Returns:
            All synchronous bars indexed by their bar index.
        """

    @abstractmethod
    def get_bars(self, staff_ind: int_staff_index) -> dict[int_bar_index, Bar]:
        """Get the collection of bars of a single staff.

        Args:
            staff_ind: the index of the staff for which we want to return the bars.

        Returns:
            All bars of a single staff indexed by their bar index..
        """

    @abstractmethod
    def get_bar(self, staff_ind: int_staff_index, bar_index: int_bar_index) -> Bar:
        """Get a single bar from a specific staff.

        Args:
            staff_ind: the index of the staff
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
            voice_strings.append("{\\voice" + voices_index_to_name[voice_ind] + ' ' + bar.lilypond_str + ' }')
        return '{<<' + ' \\new Voice '.join(voice_strings) + '>>}'

    def get_voices(self) -> dict[int_voice_index, Bar]:
        return self.voices


@dataclass(frozen=True, slots=True)
class SimpleSynchronousBars(SynchronousBars):
    """Representation of a bar across staffs.

    Args:
        bars: one bar for each staff
    """
    bars: tuple[Bar, ...]

    def get_bars(self) -> tuple[Bar, ...]:
        return self.bars

    def get_bar(self, staff_ind: int_staff_index) -> Bar:
        return self.bars[staff_ind]


@dataclass(frozen=True, slots=True)
class SimpleBarCollection(BarCollection):
    """Representation of a collection of bars contained in a dictionary.

    The bars are stored as synchronous bars, splitting them when necessary. Furthermore, the bars are stored in a
    dictionary such that we can store the bars with their dice table label instead of a numerical index.

    Args:
        synchronous_bars: the collection of synchronous bars indexed by their bar index.
    """
    synchronous_bars: dict[int_bar_index, SynchronousBars]

    def get_synchronous_bars(self) -> dict[int_bar_index, SynchronousBars]:
        return self.synchronous_bars

    def get_bars(self, staff_ind: int_staff_index) -> dict[int_bar_index, Bar]:
        return {key: sb.get_bar(staff_ind) for key, sb in self.synchronous_bars.items()}

    def get_bar(self, staff_ind: int_staff_index, bar_index: int_bar_index) -> Bar:
        return self.synchronous_bars[bar_index].get_bar(staff_ind)


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
    table by selecting bar indices by table key and staff index.
    """

    @abstractmethod
    def get_bar_index(self, table_key: str_dice_table_key, throw_ind: int,
                      staff_ind: int_staff_index | None = None) -> int:
        """Get the bar index for a specific dice table, a specified throw index and optionally a specific staff.

        Args:
            table_key: the key of the dice table we have indices for
            throw_ind: the index of the dice throw
            staff_ind: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The selected bar for this dice table, dice throw and staff.
        """

    @abstractmethod
    def get_bar_indices(self, table_key: str_dice_table_key, staff_ind: int_staff_index | None = None) -> list[int]:
        """Get the bar indices chosen for the specific dice table and staff (within that dice table).

        For a given table, this may either return the same bar indices for each staff, or a different list per staff.

        Args:
            table_key: the key of the dice table we have indices for
            staff_ind: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The selected bar for this dice table, dice throw and staff.
        """


@dataclass(slots=True, frozen=True)
class GroupedStaffsBarSelection(BarSelection):
    """Bar selection where we select the same bar indices for each staff of a dice table.

    Args:
        bar_indices: for each table key, the list of bars we want to select in the composition.
    """
    bar_indices: dict[str, list[int]]

    def get_bar_index(self, table_key: str_dice_table_key, throw_ind: int,
                      staff_ind: int_staff_index | None = None) -> int:
        return self.bar_indices[table_key][throw_ind]

    def get_bar_indices(self, table_key: str_dice_table_key, staff_ind: int_staff_index | None = None) -> list[int]:
        return self.bar_indices[table_key]


@dataclass(slots=True, frozen=True)
class PerStaffsBarSelection(BarSelection):
    """Bar selection where we may select different bar indices for each staff of a dice table.

    Args:
        bar_indices: for each table key, and for each staff, the list of bars we want to select in the composition.
    """
    bar_indices: dict[str, dict[int, list[int]]]

    def get_bar_index(self, table_key: str_dice_table_key, throw_ind: int,
                      staff_ind: int_staff_index | None = None) -> int:
        return self.bar_indices[table_key][staff_ind][throw_ind]

    def get_bar_indices(self, table_key: str_dice_table_key, staff_ind: int_staff_index| None = None) -> list[int]:
        return self.bar_indices[table_key][staff_ind]


class MidiSettings(metaclass=ABCMeta):

    @abstractmethod
    def get_midi_instrument(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> str:
        """Get the midi instrument to use for rendering the specific table and specific staff.

        Args:
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            The instrument name as a midi instrument name
        """

    @abstractmethod
    def get_min_volume(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> float:
        """Get the minimum volume to use for rendering the specific table and specific staff.

        Args:
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            The minimum volume to use.
        """

    @abstractmethod
    def get_max_volume(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> float:
        """Get the maximum volume to use for rendering the specific table and specific staff.

        Args:
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            The maximum volume to use.
        """

    @abstractmethod
    def with_updated_instrument(self, midi_instrument: str, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        """Get a version of this midi setting but with a different instrument for the given dice table and staff.

        Args:
            midi_instrument: the new instrument name to insert
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_min_volume(self, min_volume: float, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        """Get a version of this midi setting but with a different minimum volume for the given dice table and staff.

        Args:
            min_volume: the new minimum volume
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_max_volume(self, max_volume: float, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        """Get a version of this midi setting but with a different maximum volume for the given dice table and staff.

        Args:
            max_volume: the new maximum volume
            table_key: the specific table
            staff_ind: the specific staff

        Returns:
            A new instance of this midi settings.
        """


@dataclass(frozen=True, slots=True)
class SimpleMidiSettings(MidiSettings):
    """Simple lookup implementation of the midi settings.

    Args:
        midi_instruments: the instruments to use, indexed by table key and staff ind
        min_volumes: the minimum volumes to use, indexed by table key and staff ind
        max_volumes: the maximum volumes to use, indexed by table key and staff ind
    """
    midi_instruments: dict[str, dict[int, str]]
    min_volumes: dict[str, dict[int, float]]
    max_volumes: dict[str, dict[int, float]]

    def get_midi_instrument(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> str:
        return self.midi_instruments[table_key][staff_ind]

    def get_min_volume(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> float:
        return self.min_volumes[table_key][staff_ind]

    def get_max_volume(self, table_key: str_dice_table_key, staff_ind: int_staff_index) -> float:
        return self.max_volumes[table_key][staff_ind]

    def with_updated_instrument(self, midi_instrument: str, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        updated_dict = self.midi_instruments | {table_key: (self.midi_instruments[table_key] | {staff_ind: midi_instrument})}
        return type(self)(updated_dict, self.min_volumes, self.max_volumes)

    def with_updated_min_volume(self, min_volume: float, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        updated_dict = self.min_volumes | {table_key: (self.min_volumes[table_key] | {staff_ind: min_volume})}
        return type(self)(self.midi_instruments, updated_dict, self.max_volumes)

    def with_updated_max_volume(self, max_volume: float, table_key: str_dice_table_key,
                                staff_ind: int_staff_index) -> Self:
        updated_dict = self.max_volumes | {table_key: (self.max_volumes[table_key] | {staff_ind: max_volume})}
        return type(self)(self.midi_instruments, self.min_volumes, updated_dict)
