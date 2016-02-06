from collections import OrderedDict
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

    def __init__(self, name, composer_name, parts, composition_manager, page_limit_composition,
                 page_limit_measure_overview):
        """Holds basic information about a composition and is able to create various views on the composition.

        Args:
            name (str): the name of the composition
            composer_name (str): the name of the composer
            parts (list of CompositionPart): the list of parts, in the order of appearance
            composition_manager (CompositionManager): the composition manager for managing the composition scores
            page_limit_composition (int or None): if not None it indicates the page limit for compositions
            page_limit_measure_overview (int or None): if not None it indicates the page limit for the measure overviews
        """
        self.name = name
        self.composer_name = composer_name
        self.parts = parts
        self.composition_manager = composition_manager
        self.page_limit_composition = page_limit_composition
        self.page_limit_measure_overview = page_limit_measure_overview

    def get_composition_info(self):
        """Get the info necessary to recreate this composition using the composition factory.

        Returns:
            dict: with keys: composer, composition, instruments. If the instruments are all the same for all the parts
                we return a string for that single instrument
        """
        instruments = [part.instrument.name for part in self.parts]
        if len(set(instruments)) == 1:
            instruments = instruments[0]

        return {'composer': self.composer_name, 'composition': self.name,
                'instruments': instruments}

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

    def typeset_composition(self, table_indices, comments=(), midi_options=None):
        """Typeset a whole composition with all the pieces.

        Args:
            table_indices (dict): per musical part and per staff the list of indices we want to use for that part.
            comments (list of MusicBookComment): the list of comments we append at the end of the composition
            midi_options (dict with list of MidiOption objects): a dictionary with for every part in the
                composition a list with per tract additional midi options. The default is used for options set to None.

        Returns:
            LilypondBook: the lilypond book for a single whole composition
        """
        midi_options = midi_options or {}
        scores = self.composition_manager.get_scores(self.parts, table_indices, midi_options=midi_options)
        return MusicBookTypeset(self.name, scores, show_title=True, comments=comments,
                                page_limit=self.page_limit_composition).typeset()

    def get_midi_options(self):
        """Get the default midi options in use in this composition.

        The exact same data structure can be handed over to the typeset_composition function if you want to
        overwrite parts of these defaults

        Returns:
            midi_options (dict with list of MidiOption objects): a dictionary with for every part in the
                composition a list with per tract the midi options
        """
        return {part.name: part.get_midi_options() for part in self.parts}

    def get_dice_tables(self):
        """Get the dice tables used to create compositions.

        Returns:
            OrderedDict: as keys composition parts and as values the list of dice tables to be used
                for that composition part. The order is in the order of appearance of the parts.
        """
        return OrderedDict([(part.name, part.get_dice_tables()) for part in self.parts])

    def typeset_single_measure(self, part_name, table_measure_ids):
        """Typeset a single measure in this composition.

        Args:
            part_name (str): the composition part for which we want the single measure
            table_measure_ids (dict): for one or more staffs the id of the measure we want to return

        Returns:
            LilypondBook: the lilypond score for the single measure
        """
        for part in self.parts:
            if part.name == part_name:
                return part.typeset_single_measure(table_measure_ids)

    def get_duplicates(self, part_name, staff=None):
        """Get the duplicate measures in the given composition part when using the given staffs to find the duplicates.

        Args:
            part_name (str): the composition part for which we want the single measure
            staff (str): the staff to use when finding the duplicates. If None we use all the staffs.

        Returns:
            list of list of int: the duplicate measures the list of dice table ids in which that measure occurs
        """
        for part in self.parts:
            if part.name == part_name:
                return part.get_duplicates(staff=staff)

    def are_dice_tables_linked(self, part_name=None):
        """Check if the dice tables in the given part are linked or not.

        If no part name is given we return a list of booleans for all parts in the composition.

        Args:
            part_name (str): the part for which we want to check if the dice tables are linked

        Returns:
            a boolean if the dice tables are linked or not or, or a list of booleans if no part name is given.
        """
        if part_name is None:
            return [part.are_dice_tables_linked() for part in self.parts]

        for part in self.parts:
            if part.name == part_name:
                return part.are_dice_tables_linked()


class CompositionPart(object):

    def __init__(self, name, instrument, show_title=True):
        """Contains information about one part of a composition.

        Args:
            name (str): the part name
            instrument (Instrument): the instrumental information
            show_title (boolean): if we show the title of this part in the compositions
        """
        self.name = name
        self.instrument = instrument
        self.show_title = show_title

    def get_dice_tables(self):
        """Get the dice tables for the staffs (in the instrument) in this composition part

        Returns:
            dict: as keys the staffs as values the dice tables to be used for creating compositions
        """
        return self.instrument.get_dice_tables()

    def are_dice_tables_linked(self):
        """Check if the dice tables are linked or not.

        Returns:
            bool: if the dice tables are linked or not
        """
        return self.instrument.dice_tables_linked

    def get_duplicates(self, staff=None):
        """Get the duplicate measures using the given staffs to find the duplicates.

        Args:
            staff (str): the staff to use when finding the duplicates. If None we use all the staffs.

        Returns:
            list of list of int: the duplicate measures the list of dice table ids in which that measure occurs
        """
        return self.instrument.get_duplicates(staff=staff)

    def get_midi_options(self):
        """Get the default midi options in use in this composition.

        The exact same data structure can be handed over to the typeset_composition function if you want to
        overwrite parts of these defaults

        Returns:
            midi_options (list of MidiOption objects): a dictionary with for every part in the
                composition a list with per tract the midi options
        """
        return self.instrument.get_midi_options()

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from this composition part.

        Returns:
            int: the number of unique compositions
        """
        return self.instrument.count_unique_compositions()

    def get_composition_scores(self, indices, part_manager, midi_options=None):
        """Get the score used in a composition.

        Args:
            indices (dict): per staff the list of the indices to the measures we want to use for this composition.
            part_manager (CompositionPartManager): the manager we use when we want to create a composition
            midi_options (list of MidiOption): a list with per tract additional midi options.
                The default is used for options set to None.

        Returns:
            list of LilypondScore: the visual and midi score for a composition with the given indices
        """
        return self.instrument.get_composition_scores(self.name, indices, part_manager,
                                                      midi_options=midi_options, show_title=self.show_title)

    def get_measure_overview_score(self):
        """Typeset the overview of the measures.

        Returns:
            LilypondScore: the lilypond score for this composition part
        """
        return self.instrument.get_measure_overview_score(self.name, show_title=self.show_title)

    def typeset_single_measure(self, table_measure_ids):
        """Typeset a single measure in this composition.

        Args:
            table_measure_ids (dict): for one or more staffs the id of the measure we want to return

        Returns:
            LilypondBook: the lilypond score for the single measure
        """
        return self.instrument.typeset_single_measure(table_measure_ids)


class Instrument(object):

    def __init__(self, name, staffs, tempo_indication, repeats, staff_layout, bar_converter, dice_tables_linked):
        """Create an instruments information object for the given tracts.

        Args:
            name (str): the name of this instrument
            staffs (list of Staff): the list of staffs for this instrument
            tempo_indication (TempoIndication): the tempo indication for this instrument
            repeats (list of tuples of int): the bars we repeat. For example: [(0, 8), (8, 16)] indicates
                two repeats, one in which 0 to 8 is repeated and one in which 8 to 16 is repeated.
            staff_layout (StaffLayout): the staff layout used when rendering the staffs
            bar_converter (BarConverter): the bar converter to use when typesetting the staffs
            dice_tables_linked (bool): if the dice tables are linked or not. Normally when they are equal they
                are linked. If they are linked the staffs in this composition part are linked to each other.
                Measure 1 in staff one should then correspond (by default) with measure 1 in staff 2.
                If they are not linked by default the measures in both staffs should be treated independent of each
                other.
        """
        self.name = name
        self.staffs = staffs
        self.tempo_indication = tempo_indication
        self.repeats = repeats
        self.staff_layout = staff_layout
        self.bar_converter = bar_converter
        self.dice_tables_linked = dice_tables_linked

    def get_dice_tables(self):
        """Get the dice tables for the staffs in this instrument

        Returns:
            dict: as keys the staff name as values the dice tables to be used for creating compositions
        """
        return {staff.name: staff.dice_table for staff in self.staffs}

    def get_duplicates(self, staff=None):
        """Get the duplicate measures using the given staffs to find the duplicates.

        This is useful if you want to mark in the dice table all measures that have duplicates somewhere.

        Args:
            staff (str): the staff to use when finding the duplicates. If None we use all the staffs.

        Returns:
            list of list of int: the duplicate measures the list of dice table ids in which that measure occurs
        """
        from musical_games.dice_games.utils import find_duplicate_bars

        if staff:
            for st in self.staffs:
                if st.name == staff:
                    return find_duplicate_bars([st.bars])
        else:
            return find_duplicate_bars(list(s.bars for s in self.staffs))

    def get_midi_options(self):
        """Get the default midi options in use in this composition.

        The exact same data structure can be handed over to the typeset_composition function if you want to
        overwrite parts of these defaults

        Returns:
            midi_options (list of MidiOption objects): a dictionary with for every part in the
                composition a list with per tract the midi options
        """
        return list(staff.midi_options for staff in self.staffs)

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from the tracts in this instrument.

        Returns:
            int: the number of unique compositions
        """
        from musical_games.dice_games.utils import find_duplicate_bars

        if self.dice_tables_linked:
            duplicates = find_duplicate_bars(list(t.bars for t in self.staffs))
            return self.staffs[0].dice_table.count_unique_combinations(duplicates)
        else:
            prod = 1
            for tract in self.staffs:
                prod *= tract.dice_table.count_unique_combinations(find_duplicate_bars([tract.bars]))
            return prod

    def get_composition_scores(self, title, indices, part_manager, midi_options=None, show_title=True):
        """Get the scores used in a composition.

        Args:
            title (str): the title of this part
            indices (dict): per staff the list of the indices to the measures we want to use for this composition.
            part_manager (CompositionPartManager): the manager we use when we want to create a composition
            midi_options (list of MidiOption): a list with per tract additional midi options.
                The default is used for options set to None.
            show_title (boolean): if we show the title of this part or not

        Returns:
            list of LilypondScore: the visual and midi score for a composition with the given indices
        """
        bars = []
        for staff in self.staffs:
            bars.append([staff.bars.get_dice_table_indexed(measure_index) for measure_index in indices[staff.name]])
        return part_manager.get_scores(self, title, bars, midi_options=midi_options, show_title=show_title)

    def get_measure_overview_score(self, title, show_title=True):
        """Typeset the overview of the measures.

        Args:
            title (str): the title of this score
            show_title (boolean): if we show the title of this part or not

        Returns:
            LilypondScore: the lilypond score for this composition part
        """
        bars = list(staff.bars.bars for staff in self.staffs)
        music_expressions = AllBarsConcatenated(bars, self.bar_converter, end_bar='|').typeset()

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
            staff_layout=self.staff_layout,
            show_tempo_indication=False,
            show_title=show_title,
            show_bar_numbers=True
        ).typeset()
        return score

    def typeset_single_measure(self, table_measure_ids):
        """Typeset a single measure.

        This is supposed to be used to illustrate a single measure referenced in one of the dice tables. The given
        argument should contain a dictionary with as key the table we want to index and as value the id of the bars.

        If there are more staffs in this instrument than those defined in the given argument we will only render
        measures for which we have an index defined.

        The given measure ids should be in Dice Table space, that is, 1-based.

        Args:
            table_measure_ids (dice): per dice table the indices (1-based) from the dice table.

        Returns:
            LilypondBook: the lilypond book containing the visual score for one measure.

        Raises:
            ValueError: if only one measure index was given while the dice tables are not equal
        """
        used_staffs = list(filter(lambda st: st.name in table_measure_ids, self.staffs))
        bars = [[staff.bars.get_dice_table_indexed(table_measure_ids[staff.name])] for staff in used_staffs]
        music_expressions = AllBarsConcatenated(bars, self.bar_converter).typeset()

        staffs = []
        for ind, staff in enumerate(used_staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        score = VisualScoreTypeset(
            'Single measure',
            staffs,
            self.tempo_indication,
            staff_layout=self.staff_layout,
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

    def count_unique_combinations(self, duplicates):
        """Count the number of possible unique combinations over the columns.

        Duplicates in the same column will reduce the total number of combinations.

        Args:
            duplicates (list of list of int): the list of double positions. This contains
                a list holding lists with per similar measures the index of that measure

        Returns:
            int: the total number of unique combinations possible
        """
        columns = self.table.shape[1]
        total = 1
        for column_ind in range(columns):
            total *= self._get_unique_in_column(self.table[:, column_ind], duplicates)
        return total

    def _get_unique_in_column(self, column, duplicates):
        """Get a count of all the unique rows in a given column.

        The idea is that duplicates only count as one since if multiple indices in a column represent the same measure/bar,
        the composition that results is the same no matter which of those indices was chosen.

        It is possible that a same measure appears in multiple columns. These do not count as 1 since they occur
        at different positions in the final composition.

        As an implementation note, what this function does is to loop through the list of double lists
        and remove present duplicates from the given column. Every time it removes one or more duplicates it increases a
        counter. In the end it returns the sum of the length of the remaining column values and the count of the
        number of times we removed a double.

        This count of number of times we remove one or more measures is a good indicator for the number of duplicates.
        If we now remove one value or more, the unique count is still incremented by one.

        Args:
            column (ndarray): the column from which to count only the unique values
            duplicates (list of list of int): the list of duplicates. The main list contains a number of lists that
                contain the indices of double measures.

        Returns:
            int: the count of unique measures in this dice table.
        """
        nmr_double_pairs = 0

        unique_values = set(column)
        for double_list in duplicates:
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
