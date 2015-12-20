import numbers
from functools import reduce
from operator import mul
import numpy as np
from musical_games.dice_games.lilypond.base import MusicBookComment, TypesetStaffInfo
from musical_games.dice_games.lilypond.staff_builders import AllBarsConcatenated
from musical_games.dice_games.lilypond.typesetters import VisualScoreTypeset, MusicBookTypeset

__author__ = 'Robbert Harms'
__date__ = "2015-12-05"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class Composition(object):

    def __init__(self, name, parts, composition_manager, page_limit_composition, page_limit_measure_overview):
        """Holds basic information about a composition and is able to create various views on the composition.

        Args:
            name (str): the name of the composition
            parts (list of CompositionPart): the list of parts, in the order of appearance
            composition_manager (CompositionManager): the composition manager for managing the composition scores
            page_limit_composition (int or None): if not None it indicates the page limit for compositions
            page_limit_measure_overview (int or None): if not None it indicates the page limit for the measure overviews
        """
        self.name = name
        self.parts = parts
        self.composition_manager = composition_manager
        self.page_limit_composition = page_limit_composition
        self.page_limit_measure_overview = page_limit_measure_overview

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from this composition.

        Returns:
            int: the number of unique compositions
        """
        sub_counts = map(lambda v: v.count_unique_compositions(), self.parts)
        return reduce(mul, sub_counts, 1)

    def typeset_measure_overview(self):
        """Typeset the overview of the measures.

        Returns:
            LilypondBook: the lilypond book with the measures for all the parts
        """
        scores = [p.get_measure_overview_score() for p in self.parts]
        return MusicBookTypeset(self.name, scores, show_title=True,
                                page_limit=self.page_limit_measure_overview).typeset()

    def typeset_composition(self, table_indices, comments=()):
        """Typeset a whole composition with all the pieces.

        Args:
            table_indices (dict): per musical part and per dice table the list of indices we want to use for that part.
            comments (list of MusicBookComment): the list of comments we append at the end of the composition

        Returns:
            LilypondBook: the lilypond book for a single whole composition
        """
        scores = self.composition_manager.get_scores(self.parts, table_indices)
        return MusicBookTypeset(self.name, scores, show_title=True, comments=comments,
                                page_limit=self.page_limit_composition).typeset()

    def get_dice_tables(self):
        """Get the dice tables used to create compositions.

        Returns:
            dict: as keys the names of the composition parts and as values the list of dice tables to be used
                for that composition
        """
        return {part.name: part.get_dice_tables() for part in self.parts}


class CompositionPart(object):

    def __init__(self, name, instrument):
        """Contains information about one part of a composition.

        Args:
            name (str): the part name
            instrument (Instrument): the instrumental information
        """
        self.name = name
        self.instrument = instrument

    def get_dice_tables(self):
        """Get the dice tables for the staffs (in the instrument) in this composition part

        Returns:
            list of DiceTable: the dice tables to be used for creating compositions
        """
        return self.instrument.get_dice_tables()

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from this composition part.

        Returns:
            int: the number of unique compositions
        """
        return self.instrument.count_unique_compositions()

    def get_composition_scores(self, indices, part_manager):
        """Get the score used in a composition.

        Args:
            indices (list of list of int): the list of the list of indices to the measures
                we want to use for this composition. This needs one list of ints per staff
            part_manager (CompositionPartManager): the manager we use when we want to create a composition

        Returns:
            list of LilypondScore: the visual and midi score for a composition with the given indices
        """
        return self.instrument.get_composition_scores(self.name, indices, part_manager)

    def get_measure_overview_score(self):
        """Typeset the overview of the measures.

        Returns:
            LilypondScore: the lilypond score for this composition part
        """
        return self.instrument.get_measure_overview_score(self.name)

    def typeset_single_measure(self, measure_indices):
        """Typeset a single measure.

        This is supposed to be used to illustrate a single measure referenced in one of the dice tables. This
        function calls the instrument to actually compute the single measure lilypond score.

        If the dice tables are equal one measure index suffices. If the dice tables are not equal this function needs
        a measure index per tract.

        The given measure indices should be in Dice Table space, that is, 1-based.

        Args:
            measure_indices (int or list of int): the indices (1-based) from the dice table. If the dice tables of
                all the tracts are equal you only need to provide one index. Else, multiple indices (one per tract)
                are required.

        Returns:
            LilypondBook: the lilypond book containing the visual score for one measure

        Raises:
            ValueError: if only one measure index was given while the dice tables are not equal
        """
        return self.instrument.typeset_single_measure(measure_indices)


class Instrument(object):

    def __init__(self, staffs, tempo_indication, repeats, show_instrument_names, bar_converter):
        """Create an instruments information object for the given tracts.

        Args:
            staffs (list of Staff): the list of staffs for this instrument
            tempo_indication (TempoIndication): the tempo indication for this instrument
            repeats (list of tuples of int): the bars we repeat. For example: [(0, 8), (8, 16)] indicates
                two repeats, one in which 0 to 8 is repeated and one in which 8 to 16 is repeated.
            show_instrument_names (boolean): if we by default show the staff instrument names or not
            bar_converter (BarConverter): the bar converter to use when typesetting the staffs
        """
        self.staffs = staffs
        self.tempo_indication = tempo_indication
        self.repeats = repeats
        self.show_instrument_names = show_instrument_names
        self.bar_converter = bar_converter
        self.dice_tables_equal = all(tract.dice_table == self.staffs[0].dice_table for tract in self.staffs)

    def get_dice_tables(self):
        """Get the dice tables for the staffs in this instrument

        Returns:
            list of DiceTable: the dice tables to be used for creating compositions
        """
        if self.dice_tables_equal:
            return [self.staffs[0].dice_table]
        return [staff.dice_table for staff in self.staffs]

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from the tracts in this instrument.

        Returns:
            int: the number of unique compositions
        """
        from musical_games.dice_games.utils import find_double_bars

        if self.dice_tables_equal:
            doubles = find_double_bars(list(t.bars for t in self.staffs))
            return self.staffs[0].dice_table.count_unique_combinations(doubles)
        else:
            prod = 1
            for tract in self.staffs:
                prod *= tract.dice_table.count_unique_combinations(find_double_bars([tract.bars]))
            return prod

    def get_composition_scores(self, title, indices, part_manager):
        """Get the scores used in a composition.

        Args:
            title (str): the title of this part
            indices (list of list of int): the list of the list of indices to the measures
                we want to use for this composition. This needs one list of ints per staff
            part_manager (CompositionPartManager): the manager we use when we want to create a composition

        Returns:
            list of LilypondScore: the visual and midi score for a composition with the given indices
        """
        bars = []
        for staff_ind, staff in enumerate(self.staffs):
            if self.dice_tables_equal:
                staff_bars = [staff.bars.get_dice_table_indexed(measure_index) for measure_index in indices[0]]
            else:
                staff_bars = [staff.bars.get_dice_table_indexed(measure_index) for measure_index in indices[staff_ind]]
            bars.append(staff_bars)

        return part_manager.get_scores(self, title, bars)

    def get_measure_overview_score(self, title):
        """Typeset the overview of the measures.

        Args:
            title (str): the title of this score

        Returns:
            LilypondScore: the lilypond score for this composition part
        """
        bars = list(staff.bars.bars for staff in self.staffs)
        music_expressions = AllBarsConcatenated(bars, self.bar_converter).typeset()

        staffs = []
        for ind, staff in enumerate(self.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        score = VisualScoreTypeset(
            title,
            staffs,
            self.tempo_indication,
            show_instrument_names=self.show_instrument_names,
            show_tempo_indication=False,
            show_title=True,
            show_bar_numbers=True
        ).typeset()
        return score

    def typeset_single_measure(self, measure_indices):
        """Typeset a single measure.

        This is supposed to be used to illustrate a single measure referenced in one of the dice tables.

        If the dice tables are equal one measure index suffices. If the dice tables are not equal this function needs
        one measure index per tract.

        The given measure indices should be in Dice Table space, that is, 1-based.

        Args:
            measure_indices (int or list of int): the indices (1-based) from the dice table. If the dice tables of
                all the tracts are equal you only need to provide one index. Else, multiple indices (one per tract)
                are required.

        Returns:
            LilypondBook: the lilypond book containing the visual score for one measure

        Raises:
            ValueError: if only one measure index was given while the dice tables are not equal
        """
        if isinstance(measure_indices, numbers.Number):
            measure_indices = [measure_indices]

        if len(measure_indices) < len(self.staffs):
            if self.dice_tables_equal:
                measure_indices *= len(self.staffs)
            else:
                raise ValueError('The dice tables are not equal and only one measure index is given.')

        bars = list(staff.bars.get_dice_table_indexed(measure_indices[ind]) for ind, staff in enumerate(self.staffs))
        music_expressions = AllBarsConcatenated([[bars[0]], [bars[1]]], self.bar_converter).typeset()

        staffs = []
        for ind, staff in enumerate(self.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        score = VisualScoreTypeset(
            'Single measure: {}'.format(', '.join(map(str, measure_indices))),
            staffs,
            self.tempo_indication,
            show_instrument_names=self.show_instrument_names,
            show_tempo_indication=False,
            show_title=False
        ).typeset()

        return MusicBookTypeset('Single measure', [score], show_title=False).typeset()


class Staff(object):

    def __init__(self, name, dice_table, clef, bars, key_signature, time_signature, instrument_name, midi_options):
        """Information about a single staff.

        For example, you can have two of these, one for the left hand of a piece and one for the right hand
        (in the case of a piano).

        Args:
            name (str): the name of the staff
            dice_table (DiceTable): the dice table for this part
            clef (str): lilypond clef notation string. Like 'treble' or 'bass'
            bars (Bars): the Bars object containing the bars
            key_signature (KeySignature): the key signature
            time_signature (TimeSignature): the time signature
            instrument_name (str): the name of this instrument
            midi_options (MidiOptions): the container for the midi options
        """
        self.name = name
        self.dice_table = dice_table
        self.clef = clef
        self.bars = bars
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.instrument_name = instrument_name
        self.midi_options = midi_options


class Bars(object):

    def __init__(self, bars):
        """Container for the bars in use in a single tract.

        Args:
            bars (list of Bar): the list of Bar objects
        """
        self.bars = bars

    def length(self):
        """Get the number of bars in this Bars object.

        Returns:
            int: the number of bars contained in this Bars object.
        """
        return len(self.bars)

    def get_at_index(self, index):
        """Get the bar at the given index.

        This is 0-based and should not be used with the index of a bar from a DiceTable.

        Args:
            index (int): the index to return the Bar at.

        Returns:
            Bar: the bar at the given index
        """
        return self.bars[index]

    def get_dice_table_indexed(self, dice_table_index):
        """Get the bar at the given dice table index.

        This is 1-based and should be used when holding the index of a Bar from a Dice Table.

        Args:
            dice_table_index (int): the index to return the Bar at.

        Returns:
            Bar: the bar at the given index
        """
        return self.get_at_index(dice_table_index - 1)


class DiceTable(object):

    def __init__(self, table):
        """The dice table to use for playing a dice game.

        Args:
            table (ndarray): numpy array containing the dice table
        """
        self.table = table

    @property
    def rows(self):
        """Get the number of rows in this table.

        Returns:
            int: the number of rows in the table
        """
        return self.table.shape[0]

    @property
    def columns(self):
        """Get the number of columns in this table.

        Returns:
            int: the number of columns in the table
        """
        return self.table.shape[1]

    def get_row(self, row):
        """Get the elements on the given row.

        Args:
            row (int): the row we want the elements of

        Returns:
            list: the list of elements on that row
        """
        return list(self.table[row, :])

    def get_rows(self):
        """Get a list of all the rows.

        Returns:
            list of list: the list of rows in the table, from top to bottom
        """
        return list(map(self.get_row, range(self.rows)))

    def random_index(self, column, seed=None):
        """Get the index of a random row in the dice table given the given column.

        Args:
            column (int): the column number we want to get a random row index from.
            seed (int): the optional seed number to use for the random number generator

        Returns:
            int: the index to a measure for one specific column and a random row
        """
        if seed is not None:
            np.random.seed(np.uint32(seed))

        return self.table[np.random.randint(self.table.shape[0]), column]

    def random_indices(self, seed=None):
        """Get a random list of indices, one for each column.

        Args:
            seed (int): the optional seed number to use for the random number generator

        Returns:
            list: list of indices, one per column
        """
        if seed is not None:
            np.random.seed(np.uint32(seed))

        return [self.random_index(column) for column in range(self.table.shape[1])]

    def get_all_indices(self):
        """Get a sorted list of all the indices in this table.

        Returns:
            list: list of all sorted indices in this table.
        """
        return sorted(self.table.flatten())

    def column_split(self, column):
        """Split this dice table into two dice tables depending on the given column.

        We split at the given column. So if you have columns 1,2,3,4 and split on 3 you get 1,2 and 3,4.

        Args:
            column (int): the column to split on

        Returns:
            list of DiceTable: one per split
        """
        return DiceTable(self.table[:, 0:column]), DiceTable(self.table[:, column:])

    def count_unique_combinations(self, doubles):
        """Count the number of possible unique combinations over the columns.

        Doubles in the same column will reduce the total number of combinations.

        Args:
            doubles (list of list of int): the list of double positions. This contains
                a list holding lists with per similar measures the index of that measure

        Returns:
            int: the total number of unique combinations possible
        """
        columns = self.table.shape[1]
        total = 1
        for column_ind in range(columns):
            total *= self._get_unique_in_column(self.table[:, column_ind], doubles)
        return total

    def _get_unique_in_column(self, column, doubles):
        """Get a count of all the unique rows in a given column.

        The idea is that doubles only count as one since if multiple indices in a column represent the same measure/bar,
        the composition that results is the same no matter which of those indices was chosen.

        It is possible that a same measure appears in multiple columns. These do not count as 1 since they occur
        at different positions in the final composition.

        As an implementation note, what this function does is to loop through the list of double lists
        and remove present doubles from the given column. Every time it removes one or more doubles it increases a
        counter. In the end it returns the sum of the length of the remaining column values and the count of the
        number of times we removed a double.

        This count of number of times we remove one or more measures is a good indicator for the number of doubles. If
        we now remove one value or more, the unique count is still incremented by one.

        Args:
            column (ndarray): the column from which to count only the unique values
            doubles (list of list of int): the list of doubles. The main list contains a number of lists that
                contain the indices of double measures.

        Returns:
            int: the count of unique measures in this dice table.
        """
        nmr_double_pairs = 0

        unique_values = set(column)
        for double_list in doubles:
            s = unique_values.intersection(double_list)
            if len(s):
                column = [v for v in column if v not in s]
                unique_values = set(column)
                nmr_double_pairs += 1

        return len(column) + nmr_double_pairs

    def __eq__(self, other):
        return isinstance(other, self.__class__) and np.array_equal(self.table, other.table)

    def __ne__(self, other):
        return not self.__eq__(other)
