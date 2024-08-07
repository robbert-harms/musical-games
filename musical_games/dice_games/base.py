from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import math
import random
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Self, TypeAlias, Any

from frozendict import frozendict
import jinja2


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
    def get_dice_table_names(self) -> list[str_dice_table_name]:
        """Get a list of dice table names in this dice game.

        Returns:
            A list of the dice table names supported by this dice game.
        """

    @abstractmethod
    def get_staff_names(self) -> dict[str_dice_table_name, list[str_staff_name]]:
        """For each dice table name, get the staff names in the corresponding bar collection.

        This is a convenience method for getting the staff names a dice table can select. Each dice table is connected
        to a bar collection. Each of those bar collections may have one or more staffs associated with it.

        Returns:
            A dictionary mapping dice table names to list of staff names.
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
    def get_bar_collections(self) -> dict[str_dice_table_name, BarCollection]:
        """Get the collection of bars for each dice table.

        Returns:
            The collection of bars for each dice table as a bar collection object.
        """

    @abstractmethod
    def get_duplicate_dice_table_elements(self, dice_table_name: str_dice_table_name) -> list[set[DiceTableElement]]:
        """Get a list of all the duplicate bars for a specific dice table.

        For a given dice table, this should scan for duplicate measures in the musical entries corresponding to each
        element in the dice table. We return each set of duplicates as a tuple containing all the dice table elements
        having duplicates.

        Returns:
            A list of duplicate dice table elements.
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
    def get_random_bar_selection(self, seed: int = None, shuffle_staffs: bool = False) -> BarSelection:
        """Get a random bar selection we may use to create a composition.

        Args:
            shuffle_staffs: if we want to shuffle the staffs within a dice table independently.
            seed: a seed for the random number generator.

        Returns:
            A bar selection object with the selected bars to form a composition.
        """

    @abstractmethod
    def bar_selection_to_bars(self,
                              bar_selection: BarSelection) -> dict[str_dice_table_name, list[SynchronousBarSequence]]:
        """Transform a bar selection (containing bar indices) to the actual selection of synchronous bar sequences.

        The bar selection contains per dice table, and optionally per staff, the bar indices we want to use in a
        composition. This function should transform that bar selection into the actual bars, corresponding to the bar
        indices in the bar selection. Multiple selections for one bar selection element will be merged into a
        single bar sequences.

        Args:
            bar_selection: the selected bar indices contained in a bar selection

        Returns:
            For each dice table the bars to use as synchronous bar sequences.
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
    def compile_single_dice_table_element(self,
                                          table_name: str_dice_table_name,
                                          dice_table_element: DiceTableElement) -> LilypondScore:
        """Get a lilypond score with only the bar or bars selected by the given dice table element.

        Since some dice tables have select more than one bar per element, we have this method in addition to
        :meth:`compile_single_bar`. The latter only selects one specific bar, this selects all the bars selected
        by the dice table element.

        Args:
            table_name: the specific dice table to use. Names should match those of the method :meth:`get_dice_tables`.
            dice_table_element: the specific dice table element for which to look up the bars.
                Should be an element of the referred table.

        Returns:
            A lilypond score for the dice table element.
        """

    @abstractmethod
    def compile_composition_score(self,
                                  bar_selection: BarSelection,
                                  comment: str | None = None,
                                  single_page: bool = False) -> LilypondScore:
        """Compile a visual composition of this dice game using the selected bars.

        Args:
            bar_selection: the selection of bars for the composition
            comment: an optional comment for at the end of the composition
            single_page: if we want to print the overview on a single large page without page breaks.

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

    def get_dice_table_names(self) -> list[str_dice_table_name]:
        return list(self._dice_tables.keys())

    def get_staff_names(self) -> dict[str_dice_table_name, list[str_staff_name]]:
        return {k: bc.get_staff_names() for k, bc in self._bar_collections.items()}

    def get_dice_tables(self) -> dict[str_dice_table_name, DiceTable]:
        return self._dice_tables

    def get_bar_collections(self) -> dict[str_dice_table_name, BarCollection]:
        return self._bar_collections

    def get_duplicate_dice_table_elements(self, dice_table_name: str_dice_table_name) -> list[set[DiceTableElement]]:
        flat_dice_table = self._dice_tables[dice_table_name].get_elements()
        bars = self._bar_collections[dice_table_name].get_synchronous_selection(flat_dice_table)

        bars_grouped = {}
        for dice_table_element, bar in zip(flat_dice_table, bars):
            bar_elements = bars_grouped.setdefault(bar, set())
            bar_elements.add(dice_table_element)

        return [v for k, v in bars_grouped.items() if len(v) > 1]

    def count_unique_compositions(self, count_duplicates=False) -> int:
        def count_unique_bars(table_name: str, throw_ind: int):
            """Count the number of unique bars for the indicated throw index (column)."""
            dice_table_column = self._dice_tables[table_name].get_column(throw_ind)
            bars_in_column = self._bar_collections[table_name].get_synchronous_selection(dice_table_column)
            return len(set(bars_in_column))

        table_counts = []
        for table_name, table in self._dice_tables.items():
            if count_duplicates:
                table_counts.append(table.nmr_dice_values ** table.nmr_throws)
            else:
                table_counts.append(reduce(mul, [count_unique_bars(table_name, throw_ind)
                                                 for throw_ind in range(table.nmr_throws)]))
        return reduce(mul, table_counts)

    def get_random_bar_selection(self, seed: int = None, shuffle_staffs: bool = False) -> BarSelection:
        if shuffle_staffs:
            choices = {}
            for table_ind, (table_name, dice_table) in enumerate(self._dice_tables.items()):
                choices[table_name] = {}
                for staff_ind, staff_name in enumerate(self._bar_collections[table_name].get_staff_names()):
                    choices[table_name][staff_name] = dice_table.get_random_selection(seed + table_ind + staff_ind)
            return PerStaffsBarSelection(choices)
        else:
            choices = {}
            for table_ind, (table_name, dice_table) in enumerate(self._dice_tables.items()):
                choices[table_name] = dice_table.get_random_selection(seed + table_ind)
            return GroupedStaffsBarSelection(choices)

    def bar_selection_to_bars(self,
                              bar_selection: BarSelection) -> dict[str_dice_table_name, list[SynchronousBarSequence]]:
        composition_bars = {table_name: [] for table_name in self._dice_tables.keys()}

        for table_name in self._dice_tables.keys():
            staff_names = self._bar_collections[table_name].get_staff_names()

            bar_sequences_per_staff = {}
            for staff_name in staff_names:
                staff_selection = bar_selection.get_dice_table_elements(table_name, staff_name)
                selected_bars = self._bar_collections[table_name].get_bar_selection(staff_name, staff_selection)
                bar_sequences_per_staff[staff_name] = selected_bars

            complete_bars = []
            for composition_ind in range(len(bar_sequences_per_staff[staff_names[0]])):
                sync_bars = {}
                for staff_name in staff_names:
                    sync_bars[staff_name] = bar_sequences_per_staff[staff_name][composition_ind]
                complete_bars.append(SimpleSynchronousBarSequence.from_dict_of_bar_sequences(sync_bars))

            composition_bars[table_name] = complete_bars
        return composition_bars

    def get_default_midi_settings(self) -> MidiSettings:
        return self._default_midi_settings

    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        template = self._jinja2_environment.get_template('bar_overview.ly')
        return SimpleLilypondScore(template.render(bar_collections=self._bar_collections,
                                                   render_settings={'single_page': single_page}))

    def compile_single_bar(self, table_name: str_dice_table_name, bar_ind: int_bar_index) -> LilypondScore:
        template = self._jinja2_environment.get_template('single_bar.ly')
        synchronous_bar_sequence = self._bar_collections[table_name].get_synchronous_bar_sequence(bar_ind)
        return SimpleLilypondScore(template.render(table_name=table_name,
                                                   synchronous_bar_sequence=synchronous_bar_sequence))

    def compile_single_dice_table_element(self,
                                          table_name: str_dice_table_name,
                                          dice_table_element: DiceTableElement) -> LilypondScore:
        template = self._jinja2_environment.get_template('single_dice_table_element.ly')
        synchronous_bar_sequence = self._bar_collections[table_name].get_synchronous_selection([dice_table_element])[0]
        return SimpleLilypondScore(template.render(table_name=table_name,
                                                   synchronous_bar_sequence=synchronous_bar_sequence))

    def compile_composition_score(self,
                                  bar_selection: BarSelection,
                                  comment: str | None = None,
                                  single_page: bool = False) -> LilypondScore:
        template = self._jinja2_environment.get_template('composition_pdf.ly')
        composition_bars = self.bar_selection_to_bars(bar_selection)
        return SimpleLilypondScore(template.render(composition_bars=composition_bars,
                                                   render_settings={'comment': comment, 'single_page': single_page}))

    def compile_composition_audio(self, bar_selection: BarSelection,
                                  midi_settings: MidiSettings | None = None) -> LilypondScore:
        midi_settings = midi_settings or self.get_default_midi_settings()
        template = self._jinja2_environment.get_template('composition_midi.ly')
        composition_bars = self.bar_selection_to_bars(bar_selection)
        return SimpleLilypondScore(template.render(composition_bars=composition_bars, midi_settings=midi_settings))

    @staticmethod
    def _generate_jinja2_environment(data_name: str) -> jinja2.Environment:
        """Generate a standard jinja2 environment for a musical game.

        This assumes the lilypond templates for the dice game are kept in the package in the data directory:
        ``data/dice_games/<data_name>/lilypond``. In addition, it will add the lilypond utility directory to the
        loader.

        Args:
            data_name: the data name of this dice games' data

        Returns:
            A jinj2 environment to provide to the dice game.
        """
        template_loader = jinja2.ChoiceLoader([
            jinja2.PackageLoader('musical_games', f'data/dice_games/{data_name}/lilypond'),
            jinja2.PackageLoader('musical_games', 'data/lilypond_utils'),
        ])
        env_options = SimpleDiceGame._standard_jinja2_environment_options() | {'loader': template_loader}
        return jinja2.Environment(**env_options)

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

    @abstractmethod
    def get_annotation(self) -> BarAnnotation:
        """Get annotation data for this bar.

        In addition to the raw lilypond data, it is convenient to store some annotation data next to it. The exact
        data may be dice game dependent, as long as is it inherits from :class:`BarAnnotation`.

        Returns:
            A bar annotation object.
        """


class BarAnnotation(metaclass=ABCMeta):
    """Annotation data for a single bar.

    A :class:`Bar` object contains a lilypond string representing the musical data for that bar. In addition, we may
    store annotation data covering data about the lilypond data.

    The exact implementation may be different for each dice game.
    """


class BarSequence(metaclass=ABCMeta):
    """Representation of a sequence of bars.

    Some dice games have an anacrusis, or pickup beat, as part of a selected bar. To realize this, we have bar
    sequences which are tuples of bars.
    """

    @property
    @abstractmethod
    def nmr_of_bars(self) -> int:
        """Get the number of bars in this sequence.

        Returns:
            A positive integer for the number of bars in this sequence.
        """

    @abstractmethod
    def get_bars(self) -> tuple[Bar, ...]:
        """Get the bars of this bar sequence.

        Returns:
            A tuple of bars.
        """

    @abstractmethod
    def get_bar(self, sequence_ind: int) -> Bar:
        """Get the bar at the indicated sequence id.

        Returns:
            The bar at the given sequence position.
        """


class SynchronousBar(metaclass=ABCMeta):
    """Representation of a tuple of bars played synchronously across staffs.

    Suppose that a piece has a piano and a violin, then at each time point there are three bars being played, left and
    right hand piano and the violin. These synchronous bars are connected in this class.
    """

    @abstractmethod
    def get_staff_names(self) -> list[str_staff_name]:
        """Get the names of the staffs stored in this synchronous bar.

        Returns:
            The names of the staffs
        """

    @abstractmethod
    def get_staffs(self) -> dict[str_staff_name, Bar]:
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


class SynchronousBarSequence(metaclass=ABCMeta):
    """Representation of a tuple of bar sequences played synchronously across staffs.

    This is similar to :class:`SynchronousBar` except that it takes bar sequences as input, not single bars.
    """

    @property
    @abstractmethod
    def nmr_bars_in_sequence(self) -> int:
        """Check how many bars there are in sequence.

        Returns:
            A positive integer with the number of bars in a sequence on one staff.
        """

    @abstractmethod
    def get_staff_names(self) -> list[str_staff_name]:
        """Get the names of the staffs stored in this synchronous bar sequence.

        Returns:
            The names of the staffs
        """

    @abstractmethod
    def get_staffs(self) -> dict[str_staff_name, BarSequence]:
        """Get the collection of bar sequences being played at the same time.

        Returns:
            The bar sequences across staves.
        """

    @abstractmethod
    def get_synchronous_bars(self) -> list[SynchronousBar]:
        """Get the bar sequences as a list of synchronous bars.

        Returns:
            A list of synchronous bars.
        """

    @abstractmethod
    def get_bar_sequence(self, staff_name: str_staff_name) -> BarSequence:
        """Get a single bar sequence from a single staff.

        Args:
            staff_name: the name of the staff for which you want the bar.

        Returns:
            The bar sequence of that staff.
        """


class BarCollection(metaclass=ABCMeta):
    """Collection of synchronous bar sequences.

    The bars are expected to be stored in a dictionary mapping bar indices to bars.
    """

    @property
    @abstractmethod
    def nmr_bars(self) -> int:
        """The number of bars in this bar collection.

        Returns:
            The number of bars in this bar collection (0-indiced).
        """

    @property
    @abstractmethod
    def maximum_bar_ind(self) -> int:
        """The maximum bar index, 1 + number of bars.

        Returns:
            The maximum bar index. Since the bars start counting at 1, this is one more than the number of bars.
        """

    @abstractmethod
    def get_synchronous_bar_sequences(self) -> dict[int_bar_index, SynchronousBarSequence]:
        """Get the collection of all synchronous bar sequences.

        Returns:
            All synchronous bar sequences indexed by their bar index.
        """

    @abstractmethod
    def get_synchronous_bar_sequence(self, bar_index: int_bar_index) -> SynchronousBarSequence:
        """Get a synchronous bar sequence at the specified bar index.

        Args:
            bar_index: the index of the bar to retrieve.

        Returns:
            The synchronous bar sequence at that bar index.
        """

    @abstractmethod
    def get_staff_names(self) -> list[str_staff_name]:
        """Get the names of the staffs stored in the synchronous bar sequences.

        Returns:
            The names of the staffs.
        """

    @abstractmethod
    def get_bar_sequences(self, staff_name: str_staff_name) -> dict[int_bar_index, BarSequence]:
        """Get the collection of bar sequences of a single staff.

        Args:
            staff_name: the name of the staff for which we want to return the bars.

        Returns:
            All bars of a single staff indexed by their bar index.
        """

    @abstractmethod
    def get_bar_sequence(self, staff_name: str_staff_name, bar_index: int_bar_index) -> BarSequence:
        """Get a single bar sequence from a specific staff.

        Args:
            staff_name: the name of the staff
            bar_index: the index of the bar

        Returns:
            The specific bar sequence in the given staff and bar index locations.
        """

    @abstractmethod
    def get_synchronous_selection(self, dice_table_elements: list[DiceTableElement]) -> list[SynchronousBarSequence]:
        """Convert a selection of dice table elements into a list of synchronous bar sequences.

        If a dice table element points to multiple consecutive synchronous bars, we concatenate these into a
        synchronous bar sequence.

        Args:
            dice_table_elements: the dice table elements we wish to lookup

        Returns:
            The synchronous bar sequences for each dice table element in the list
        """

    @abstractmethod
    def get_bar_selection(self,
                          staff_name: str_staff_name,
                          dice_table_elements: list[DiceTableElement]) -> list[BarSequence]:
        """Convert a selection of dice table elements into a list of bar sequences.

        Since each dice table element may point to multiple consecutive bars, we need to return a bar sequence.

        Args:
            dice_table_elements: the dice table elements we wish to lookup
            staff_name: only return the values of this specific staff.

        Returns:
            The selection of bar sequences for each dice table element and the specific staff
        """


@dataclass(frozen=True, slots=True)
class SimpleBar(Bar):
    """Dataclass representation of a single bar, of a single staff.

    Args:
        lilypond_str: the lilypond string representation of this bar
        annotation: optional bar annotation object.
    """
    lilypond_str: str
    annotation: BarAnnotation | None = None

    def get_annotation(self) -> BarAnnotation:
        return self.annotation


@dataclass(frozen=True, slots=True)
class SimpleBarSequence(BarSequence):
    """Dataclass representation of a single bar sequence.

    Args:
        bars: the tuple of bars this sequence is made of.
    """
    bars: tuple[Bar, ...]

    @classmethod
    def from_bar_sequences(cls, bar_sequences: list[BarSequence]) -> Self:
        """Generate a bar sequence from a list of bar sequences.

        This will concatenate all the bars from the sequences into one new sequence.

        Args:
            bar_sequences: the bar sequences to concatenate

        Returns:
            A new concatenated bar sequence
        """
        bars = []
        for bar_sequence in bar_sequences:
            bars.extend(bar_sequence.get_bars())
        return cls(tuple(bars))

    @property
    def nmr_of_bars(self) -> int:
        return len(self.bars)

    def get_bars(self) -> tuple[Bar, ...]:
        return self.bars

    def get_bar(self, sequence_ind: int) -> Bar:
        return self.bars[sequence_ind]


@dataclass(frozen=True, slots=True)
class SimpleSynchronousBar(SynchronousBar):
    """Representation of a bar across staffs.

    Args:
        bars: the bar sequences per staff.
    """
    bars: frozendict[str_staff_name, Bar]

    def __post_init__(self):
        if not isinstance(self.bars, frozendict):
            raise ValueError('Expects bars to be of type frozendict.')

    def get_staff_names(self) -> list[str_staff_name]:
        return list(self.bars.keys())

    def get_staffs(self) -> dict[str_staff_name, Bar]:
        return dict(self.bars)

    def get_bar(self, staff_name: str_staff_name) -> Bar:
        return self.bars[staff_name]

    def get_bars(self) -> list[Bar]:
        return list(self.bars.values())


@dataclass(frozen=True, slots=True)
class SimpleSynchronousBarSequence(SynchronousBarSequence):
    """Representation of a synchronous bar sequence.

    Args:
        synchronous_bars: sequence of synchronous bars
    """
    synchronous_bars: tuple[SynchronousBar, ...]

    @classmethod
    def from_synchronous_bar_sequences(cls, synchronous_bar_sequences: list[SynchronousBarSequence]) -> Self:
        """Merge a list of synchronous bar sequences into a single synchronous bar sequence.

        Args:
            synchronous_bar_sequences: a list of synchronous bar sequences which we will concatenate.

        Returns:
            A new object of this class with the merged bars.
        """
        sync_bars = []
        for synchronous_bar_sequence in synchronous_bar_sequences:
            sync_bars.extend(synchronous_bar_sequence.get_synchronous_bars())
        return cls(tuple(sync_bars))

    @classmethod
    def from_dict_of_bar_sequences(cls, staff_to_bar_sequences: dict[str_staff_name, BarSequence]) -> Self:
        """Load a simple synchronous bar from a dictionary of staffs to bar sequences.

        This expects all the bar sequences to be of the same length.

        Args:
            staff_to_bar_sequences: a dictionary mapping staff names to bar sequences

        Returns:
            A new object of this class with bars in the right format
        """
        if not len(staff_to_bar_sequences):
            return cls(tuple())

        synchronous_bars = []
        for ind in range(staff_to_bar_sequences[list(staff_to_bar_sequences.keys())[0]].nmr_of_bars):
            bars_by_staff = {}
            for staff_name, bar_sequence in staff_to_bar_sequences.items():
                bars_by_staff[staff_name] = bar_sequence.get_bar(ind)
            synchronous_bars.append(SimpleSynchronousBar(frozendict(bars_by_staff)))
        return cls(tuple(synchronous_bars))

    @property
    def nmr_bars_in_sequence(self) -> int:
        return len(self.synchronous_bars)

    def get_staff_names(self) -> list[str_staff_name]:
        if not len(self.synchronous_bars):
            return []
        return self.synchronous_bars[0].get_staff_names()

    def get_staffs(self) -> dict[str_staff_name, BarSequence]:
        return {staff_name: self.get_bar_sequence(staff_name) for staff_name in self.get_staff_names()}

    def get_synchronous_bars(self) -> list[SynchronousBar]:
        return list(self.synchronous_bars)

    def get_bar_sequence(self, staff_name: str_staff_name) -> BarSequence:
        bars = []
        for ind in range(self.nmr_bars_in_sequence):
            bars.append(self.synchronous_bars[ind].get_bar(staff_name))
        return SimpleBarSequence(tuple(bars))


@dataclass(frozen=True, slots=True)
class SimpleBarCollection(BarCollection):
    """Representation of a collection of bars contained in a dictionary.

    The bars are stored in a dictionary such that we can store the bars with their dice table label instead
    of a numerical index.

    Args:
        bar_collection: the collection of synchronous bar sequences indexed by their bar index.
    """
    bar_collection: dict[int_bar_index, SynchronousBarSequence]

    @property
    def nmr_bars(self) -> int:
        return len(self.bar_collection)

    @property
    def maximum_bar_ind(self) -> int:
        return self.nmr_bars + 1

    def get_synchronous_bar_sequences(self) -> dict[int_bar_index, SynchronousBarSequence]:
        return self.bar_collection

    def get_synchronous_bar_sequence(self, bar_index: int_bar_index) -> SynchronousBarSequence:
        return self.bar_collection[bar_index]

    def get_staff_names(self) -> list[str_staff_name]:
        if self.nmr_bars == 0:
            return []
        first_sync_bar = self.bar_collection[list(self.bar_collection.keys())[0]]
        return first_sync_bar.get_staff_names()

    def get_bar_sequences(self, staff_name: str_staff_name) -> dict[int_bar_index, BarSequence]:
        bar_sequences = {}
        for bar_index, sync_bar_sequence in self.bar_collection.items():
            bar_sequences[bar_index] = sync_bar_sequence.get_bar_sequence(staff_name)
        return bar_sequences

    def get_bar_sequence(self, staff_name: str_staff_name, bar_index: int_bar_index) -> BarSequence:
        return self.bar_collection[bar_index].get_bar_sequence(staff_name)

    def get_synchronous_selection(self, dice_table_elements: list[DiceTableElement]) -> list[SynchronousBarSequence]:
        bars = []
        for element in dice_table_elements:
            bar_tuplets = []
            for bar_index in element.get_bar_indices():
                bar_tuplets.append(self.get_synchronous_bar_sequence(bar_index))
            bars.append(SimpleSynchronousBarSequence.from_synchronous_bar_sequences(bar_tuplets))
        return bars

    def get_bar_selection(self,
                          staff_name: str_staff_name,
                          dice_table_elements: list[DiceTableElement]) -> list[BarSequence]:
        bars = []
        for element in dice_table_elements:
            bar_tuplets = []
            for bar_index in element.get_bar_indices():
                bar_tuplets.append(self.get_bar_sequence(staff_name, bar_index))
            bars.append(SimpleBarSequence.from_bar_sequences(bar_tuplets))
        return bars


class DiceTable(metaclass=ABCMeta):
    """Representation of a dice table used in playing the dice games.

    This assumes all entries in the dice game tables are one or more bar indices mapping to a bars in the bar table.

    Dice tables may select multiple bars per dice throw. This is used in some of the games, for instance Gerlach.
    """

    @property
    @abstractmethod
    def shape(self) -> tuple[int, int]:
        """Get the shape of this dice table.

        Returns:
            A tuple with the number of rows and columns.
        """

    @property
    @abstractmethod
    def max_measures_per_throw(self) -> int:
        """Get the maximum number of measures selected in the entire dice table.

        Some dice tables select more than one measure per dice table element. This gets the maximum in the entire table.
        """

    @property
    @abstractmethod
    def nmr_dices(self) -> int:
        """Get the number of dices this table needs."""

    @property
    @abstractmethod
    def min_dice_value(self) -> int:
        """Get the minimum dice value needed to select rows from this dice table."""

    @property
    @abstractmethod
    def max_dice_value(self) -> int:
        """Get the maximum dice value needed to select rows from this dice table."""

    @property
    @abstractmethod
    def nmr_dice_values(self) -> int:
        """Get the number of dice values this table expects."""

    @property
    @abstractmethod
    def nmr_throws(self) -> int:
        """Get the maximum number of throws needed to select all the columns from this dice table."""

    @abstractmethod
    def get_element(self, row: int, column: int) -> DiceTableElement:
        """Get the dice table element at the specified location.

        Args:
            row: the row index
            column: the column index

        Returns:
            The dice table element
        """

    @abstractmethod
    def get_dice_throw(self, dice_number: int, column: int) -> DiceTableElement:
        """Get the dice table element for the indicated dice value.

        This expects a number in [1, 6] for a single dice, and between [2, 12] for a double dice.

        Args:
            dice_number: the thrown dice number
            column: the column index

        Returns:
            The dice table element
        """

    @abstractmethod
    def get_elements(self) -> list[DiceTableElement]:
        """Get a list of all the dice table elements.

        Returns:
            A list of all the dice table elements
        """

    @abstractmethod
    def list_rows(self) -> list[list[DiceTableElement]]:
        """Get a list with the list of row values.

        This returns a row view of the dice table, with for each row a list of dice table elements in the row.

        Returns:
            A row view of the dice table.
        """

    @abstractmethod
    def list_columns(self) -> list[list[DiceTableElement]]:
        """Get a list with the list of column values

        This returns a column view of the dice table, with for each column a list of dice table elements in the column.

        Returns:
            A column view of the dice table.
        """

    @abstractmethod
    def get_column(self, column_ind: int) -> list[DiceTableElement]:
        """Get the column of the dice table at the indicated index.

        Args:
            column_ind: the index of the column (0 based)

        Returns:
            The dice game elements in the indicated column
        """

    @abstractmethod
    def get_row(self, row_ind: int) -> list[DiceTableElement]:
        """Get the row of the dice table at the indicated index.

        Args:
            row_ind: the index of the row (0 based)

        Returns:
            The dice game elements in the indicated row
        """

    @abstractmethod
    def get_random_selection(self, seed: int = None) -> list[DiceTableElement]:
        """Get a random selection of bar numbers

        Returns:
            A list of random bar numbers from the table
        """


class DiceTableElement(metaclass=ABCMeta):
    """Representation of an element in a dice table."""

    @property
    @abstractmethod
    def row_ind(self) -> int:
        """Get the row index of this selection.

        Returns:
            The row from which this bar selection was made.
        """

    @property
    @abstractmethod
    def column_ind(self) -> int:
        """Get the column index of this selection.

        Returns:
            The column from which this bar selection was made.
        """

    @property
    @abstractmethod
    def nmr_bars_selected(self) -> int:
        """Get the number of bars selected by this selection.

        Returns:
            The number of bars selected by this measure.
        """

    @abstractmethod
    def get_bar_indices(self) -> tuple[int_bar_index, ...]:
        """Get the bar indices.

        Returns:
            The tuple of bars. This may contain only one element in the case of single selection.
        """


@dataclass(frozen=True, slots=True)
class SimpleDiceTableElement(DiceTableElement):
    """Dataclass implementation of the dice table element selection.

    Args:
        row: the row from which this element was selected
        column: the column from which this element was selected
        bar_indices: the selected bar indices
    """
    row: int
    column: int
    bar_indices: tuple[int_bar_index, ...]

    @property
    def row_ind(self) -> int:
        return self.row

    @property
    def column_ind(self) -> int:
        return self.column

    @property
    def nmr_bars_selected(self) -> int:
        return len(self.bar_indices)

    def get_bar_indices(self) -> tuple[int_bar_index, ...]:
        return self.bar_indices


@dataclass(slots=True, frozen=True)
class SimpleDiceTable(DiceTable):
    """Implementation of a dice table.

    Args:
        table: the dice table as a list of rows, with for each row the dice table elements
        max_measures_per_throw: the maximum selected measures in the dice table.
    """
    table: list[list[DiceTableElement]]
    max_measures_per_throw: int

    @classmethod
    def from_lists(cls, array: list[list[int_bar_index | tuple[int_bar_index, ...]]]) -> Self:
        """Load this dice table from a simple list table of indices.

        Args:
            array: array with for each element one or more bar indices.

        Returns:
            An instance of this class.
        """
        table = []
        max_measures_per_throw = 1

        for row_ind, row in enumerate(array):
            table_column = []
            for column_ind, value in enumerate(row):
                value_tuple = value
                if isinstance(value, int_bar_index):
                    value_tuple = (value,)
                table_column.append(SimpleDiceTableElement(row_ind, column_ind, value_tuple))

                if len(value_tuple) > max_measures_per_throw:
                    max_measures_per_throw = len(value_tuple)

            table.append(table_column)

        return cls(table, max_measures_per_throw)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.table), len(self.table[0])

    @property
    def nmr_dices(self) -> int:
        return math.ceil(len(self.table) / 6)

    @property
    def min_dice_value(self) -> int:
        return self.nmr_dices

    @property
    def max_dice_value(self) -> int:
        return len(self.table) + (self.nmr_dices - 1)

    @property
    def nmr_dice_values(self) -> int:
        return self.max_dice_value - (self.nmr_dices - 1)

    @property
    def nmr_throws(self) -> int:
        return len(self.table[0])

    def get_element(self, row: int, column: int) -> DiceTableElement:
        return self.table[row][column]

    def get_dice_throw(self, dice_number: int, column: int) -> DiceTableElement:
        return self.get_element(dice_number - self.nmr_dices, column)

    def get_elements(self) -> list[DiceTableElement]:
        elements = []
        for row in self.table:
            for element in row:
                elements.append(element)
        return elements

    def list_rows(self) -> list[list[DiceTableElement]]:
        return self.table

    def list_columns(self) -> list[list[DiceTableElement]]:
        columns = []
        for column_ind in range(len(self.table[0])):
            column = []
            for row in self.table:
                column.append(row[column_ind])
            columns.append(column)
        return columns

    def get_column(self, column_ind: int) -> list[DiceTableElement]:
        return self.list_columns()[column_ind]

    def get_row(self, row_ind: int) -> list[DiceTableElement]:
        return self.list_rows()[row_ind]

    def get_random_selection(self, seed: int = None) -> list[DiceTableElement]:
        random.seed(seed)
        max_val = self.shape[0] - 1
        selected_elements = []
        for throw_ind in range(self.nmr_throws):
            dice_throw = random.randint(0, max_val)
            selected_elements.append(self.get_element(dice_throw, throw_ind))
        return selected_elements


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
    def get_dice_table_element(self,
                               table_name: str_dice_table_name,
                               throw_ind: int,
                               staff_name: str_staff_name | None = None) -> DiceTableElement:
        """Get the dice table element for a specific dice table, throw index and optionally a specific staff.

        Args:
            table_name: the name of the dice table we have indices for
            throw_ind: the index of the dice throw
            staff_name: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The dice table elements for this dice table, dice throw and staff.
        """

    @abstractmethod
    def get_dice_table_elements(self,
                                table_name: str_dice_table_name,
                                staff_name: str_staff_name | None = None) -> list[DiceTableElement]:
        """Get the dice table elements chosen for the specific dice table and staff (within that dice table).

        For a given table, this may either return the same bar indices for each staff, or a different list per staff.

        Args:
            table_name: the name of the dice table we have indices for
            staff_name: optionally, within the table, the staff for which we are selecting bar indices.

        Returns:
            The selected dice table elements for this dice table, dice throw and staff.
        """


@dataclass(slots=True, frozen=True)
class GroupedStaffsBarSelection(BarSelection):
    """Bar selection where we select the same bar indices for each staff of a dice table.

    Args:
        dice_table_elements: for each table key, the list of dice table elements we want to select in the composition.
    """
    dice_table_elements: dict[str_dice_table_name, list[DiceTableElement]]

    def get_dice_table_element(self,
                               table_name: str_dice_table_name,
                               throw_ind: int,
                               staff_name: str_staff_name | None = None) -> DiceTableElement:
       return self.dice_table_elements[table_name][throw_ind]

    def get_dice_table_elements(self,
                                table_name: str_dice_table_name,
                                staff_name: str_staff_name | None = None) -> list[DiceTableElement]:
        return self.dice_table_elements[table_name]


@dataclass(slots=True, frozen=True)
class PerStaffsBarSelection(BarSelection):
    """Bar selection where we may select different bar indices for each staff of a dice table.

    Args:
        dice_table_elements: for each table key, and for each staff, the list of bars we want to
            select in the composition.
    """
    dice_table_elements: dict[str_dice_table_name, dict[str_staff_name, list[DiceTableElement]]]

    def get_dice_table_element(self,
                               table_name: str_dice_table_name,
                               throw_ind: int,
                               staff_name: str_staff_name | None = None) -> DiceTableElement:
        return self.dice_table_elements[table_name][staff_name][throw_ind]

    def get_dice_table_elements(self,
                                table_name: str_dice_table_name,
                                staff_name: str_staff_name | None = None) -> list[DiceTableElement]:
        return self.dice_table_elements[table_name][staff_name]


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
    def with_updated_instrument(self,
                                midi_instrument: str,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        """Get a version of this midi setting but with a different instrument.

        If no dice table name and/or staff name is provided, we apply the update to respectively all available
        tables and/or staffs.

        Args:
            midi_instrument: the new instrument name to insert
            table_name: a specific table or list of tables
            staff_name: a specific staff or list of staffs

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_min_volume(self, min_volume: float,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        """Get a version of this midi setting but with a different minimum volume.

        If no dice table name and/or staff name is provided, we apply the update to respectively all available
        tables and/or staffs.

        Args:
            min_volume: the new minimum volume
            table_name: a specific table or list of tables
            staff_name: a specific staff or list of staffs

        Returns:
            A new instance of this midi settings.
        """

    @abstractmethod
    def with_updated_max_volume(self, max_volume: float,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        """Get a version of this midi setting but with a different maximum volume.

        If no dice table name and/or staff name is provided, we apply the update to respectively all available
        tables and/or staffs.

        Args:
            max_volume: the new maximum volume
            table_name: a specific table or list of tables
            staff_name: a specific staff or list of staffs

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

    def with_updated_instrument(self,
                                midi_instrument: str,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        return type(self)(self._update_nested_dict(self.midi_instruments, midi_instrument, table_name, staff_name),
                          self.min_volumes, self.max_volumes)

    def with_updated_min_volume(self, min_volume: float,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        return type(self)(self.midi_instruments,
                          self._update_nested_dict(self.min_volumes, min_volume, table_name, staff_name),
                          self.max_volumes)

    def with_updated_max_volume(self, max_volume: float,
                                table_name: str_dice_table_name | list[str_dice_table_name] | None = None,
                                staff_name: str_staff_name | list[str_staff_name] | None = None) -> Self:
        return type(self)(self.midi_instruments,
                          self.min_volumes,
                          self._update_nested_dict(self.max_volumes, max_volume, table_name, staff_name))

    def _update_nested_dict(self,
                            dict_to_update: dict[str_dice_table_name, dict[str_staff_name, Any]],
                            new_value: Any,
                            table_names: str_dice_table_name | list[str_dice_table_name] | None,
                            staff_names: str_staff_name | list[str_staff_name] | None):
        """Update one of the midi settings dictionary with a new value.

        Args:
            dict_to_update: the dictionary to update
            new_value: the new value to insert for the given table or staff
            table_names: the tables to update
            staff_names: the staffs to update
        """
        def get_updated_dict(dict_to_update, table_name, staff_name, new_value):
            return dict_to_update | {table_name: (dict_to_update[table_name] | {staff_name: new_value})}

        if table_names is None:
            tables = list(self.midi_instruments.keys())
        elif isinstance(table_names, str):
            tables = [table_names]
        else:
            tables = table_names

        updated_dict = dict_to_update
        for table_name in tables:
            if staff_names is None:
                staffs = list(dict_to_update[table_name].keys())
            elif isinstance(staff_names, str):
                staffs = [staff_names]
            else:
                staffs = staff_names

            for staff_name in staffs:
                if staff_name in dict_to_update[table_name]:
                    updated_dict = get_updated_dict(updated_dict, table_name, staff_name, new_value)

        return updated_dict
