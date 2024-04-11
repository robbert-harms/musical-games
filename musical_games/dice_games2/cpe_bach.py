__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from functools import reduce
from operator import mul

import jinja2
import numpy as np

from musical_games.dice_games2.base import DiceGame, SimpleBarCollection, SimpleSynchronousBars, \
    SimpleBar, SimpleDiceTable, SimpleLilypondScore, LilypondScore, DiceTable, BarCollection, BarSelection, \
    GroupedStaffsBarSelection, MidiSettings, SimpleMidiSettings, Bar


class CPEBachCounterpoint(DiceGame):

    def __init__(self):
        """Implementation of a Counterpoint dice by C.P.E. Bach.

        In this dice game, the right hand and left hand of the piano piece are shuffled independently by two
        dice tables.
        """
        self._author = 'C.P.E. Bach'
        self._title = 'Counterpoint'
        self._dice_tables = {
            'treble': SimpleDiceTable(np.array([
                [1, 10, 19, 28, 37, 46],
                [2, 11, 20, 29, 38, 47],
                [3, 12, 21, 30, 39, 48],
                [4, 13, 22, 31, 40, 49],
                [5, 14, 23, 32, 41, 50],
                [6, 15, 24, 33, 42, 51],
                [7, 16, 25, 34, 43, 52],
                [8, 17, 26, 35, 44, 53],
                [9, 18, 27, 36, 45, 54]])),
            'bass': SimpleDiceTable(np.array([
                [1, 10, 19, 28, 37, 46],
                [2, 11, 20, 29, 38, 47],
                [3, 12, 21, 30, 39, 48],
                [4, 13, 22, 31, 40, 49],
                [5, 14, 23, 32, 41, 50],
                [6, 15, 24, 33, 42, 51],
                [7, 16, 25, 34, 43, 52],
                [8, 17, 26, 35, 44, 53],
                [9, 18, 27, 36, 45, 54]])),
        }
        self._bar_collection = self._get_bar_collection()
        self._table_key_to_staff = {'treble': 0, 'bass': 1}

        self._jinja2_environment_options = dict(
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
        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games2/cpe_bach_counterpoint/lilypond')
        env_options = self._jinja2_environment_options | {'loader': template_loader}
        self._jinja2_env = jinja2.Environment(**env_options)

    @property
    def author(self) -> str:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    def get_dice_tables(self) -> dict[str, DiceTable]:
        return self._dice_tables

    def get_all_duplicate_bars(self, table_key: str) -> list[set[int]]:
        bars = self._bar_collection.get_bars(self._table_key_to_staff[table_key])

        bars_by_lilypond = {}
        for bar_ind, bar in bars.items():
            bar_indices = bars_by_lilypond.setdefault(bar.lilypond_str, set())
            bar_indices.add(bar_ind)

        return [v for k, v in bars_by_lilypond.items() if len(v) > 1]

    def count_unique_compositions(self, count_duplicates=False) -> int:
        def count_unique_bars(table_key: str, bar_numbers: list[int]):
            """Count the number of unique bars in the provided list of bar numbers."""
            bars_of_table = self._bar_collection.get_bars(self._table_key_to_staff[table_key])
            bars = [bars_of_table[bar_number].lilypond_str for bar_number in bar_numbers]
            return len(set(bars))

        table_counts = []
        for table_key, table in self._dice_tables.items():
            if count_duplicates:
                table_counts.append(table.max_dice_value ** table.nmr_throws)
            else:
                table_counts.append(reduce(mul, [count_unique_bars(table_key, column)
                                                 for column in table.list_columns()]))
        return reduce(mul, table_counts)

    def get_nmr_staffs_per_table(self) -> dict[str, int]:
        return {k: 1 for k in self._dice_tables}

    def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
        choices = {}
        for table_key, dice_table in self._dice_tables.items():
            choices[table_key] = dice_table.get_random_selection(seed)
        return GroupedStaffsBarSelection(choices)

    def get_default_midi_settings(self) -> MidiSettings:
        return SimpleMidiSettings(
            {'treble': {0: 'acoustic grand', 1: 'test'}, 'bass': {0: 'acoustic grand'}},
            {'treble': {0: 0}, 'bass': {0: 0}},
            {'treble': {0: 1}, 'bass': {0: 0.75}})

    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        template = self._jinja2_env.get_template('bar_overview.ly')
        return SimpleLilypondScore(template.render(bar_collection=self._bar_collection,
                                                   render_settings={'single_page': single_page}))

    def compile_single_bar(self, table_key: str, bar_ind: int) -> LilypondScore:
        template = self._jinja2_env.get_template('single_bar.ly')
        bar = self._bar_collection.get_bars(self._table_key_to_staff[table_key])[bar_ind]
        return SimpleLilypondScore(template.render(clef=table_key, bar=bar))

    def compile_composition_score(self, bar_selection: BarSelection, comment: str | None = None) -> LilypondScore:
        template = self._jinja2_env.get_template('composition_pdf.ly')
        return SimpleLilypondScore(template.render(composition_bars=self._bar_selection_to_bars(bar_selection),
                                                   render_settings={'comment': comment}))

    def compile_composition_audio(self, bar_selection: BarSelection,
                                  midi_settings: MidiSettings | None = None) -> LilypondScore:
        midi_settings = midi_settings or self.get_default_midi_settings()
        template = self._jinja2_env.get_template('composition_midi.ly')
        return SimpleLilypondScore(template.render(composition_bars=self._bar_selection_to_bars(bar_selection),
                                                   midi_settings=midi_settings))

    def _bar_selection_to_bars(self, bar_selection: BarSelection) -> dict:
        """Transform a bar selection (containing indices) to the actual selection of bars.

        The bar selection contains per dice table, and optionally per staff, the bar indices we want to use in a
        composition. This function should select from the collection of bars hold in this dice game the bars
        corresponding to the bar indices in the bar selection.

        Args:
            bar_selection: the selected bar indices contained in a bar selection

        Returns:
            A dictionary of any form, as usable by the composition templates in this dice game.
        """
        composition_bars = {
            'treble': [],
            'bass': []
        }
        for table_key in self._dice_tables.keys():
            for throw_ind in range(self._dice_tables[table_key].nmr_throws):
                bar_ind = bar_selection.get_bar_index(table_key, throw_ind)
                bar = self._bar_collection.get_bar(self._table_key_to_staff[table_key], bar_ind)
                composition_bars[table_key].append(bar)
        return composition_bars

    @staticmethod
    def _get_bar_collection() -> BarCollection:
        """Get the collection of bars for this dice game.

        Returns:
            The bars for this dice game as a synchronous bar collection. The first element of each synchronous bar
            is for the treble and the first dice table, the second is for the bass and the second dice table.
        """
        return SimpleBarCollection({
            1: SimpleSynchronousBars((SimpleBar("e''4 g'' e'' c''"), SimpleBar("r2 c'4 c'"))),
            2: SimpleSynchronousBars((SimpleBar("r8 e''8 g'' [f''] e'' [g''] e'' c''"), SimpleBar("c'2. c'4"))),
            3: SimpleSynchronousBars((SimpleBar("e''2. c''4"), SimpleBar("c'4 e'8 d'8 c'4 c'4"))),
            4: SimpleSynchronousBars((SimpleBar("c''4 g' e'' c''"), SimpleBar("c2 c'2"))),
            5: SimpleSynchronousBars((SimpleBar("r4 c''8 d'' e''4 c''4"), SimpleBar("r2 c'2"))),
            6: SimpleSynchronousBars(
                (SimpleBar("e''8 [f''] g'' [f''] f'' [e''] e'' c''"), SimpleBar("r4 e8 d c4 c'4"))),
            7: SimpleSynchronousBars((SimpleBar("c''2 e''2"), SimpleBar("c'1"))),
            8: SimpleSynchronousBars((SimpleBar("r8 c''8 c'' [d''] e'' [e''] d'' c''"), SimpleBar("c4 e8 g8 c'4 c'"))),
            9: SimpleSynchronousBars(
                (SimpleBar("c''4 c''8 [d''] e'' [d''] e'' c''"), SimpleBar("c'8 [c8] e g c'4 c'"))),
            10: SimpleSynchronousBars((SimpleBar("d''4 g' g''2"), SimpleBar("c'4 b8 a b4 g"))),
            11: SimpleSynchronousBars((SimpleBar("g''8 [a''] g'' fis'' g''2"), SimpleBar("c'4 c' b b"))),
            12: SimpleSynchronousBars((SimpleBar("e''8 [g'] g'' fis'' g''2"), SimpleBar("c'8 [c'8] b [a] c' [b] a g"))),
            13: SimpleSynchronousBars((SimpleBar("d''4 d'' g''2"), SimpleBar("c'4 b8 [a] b [d'] b g"))),
            14: SimpleSynchronousBars((SimpleBar("d''4 g''8 fis''8 g''2"), SimpleBar("c'4 c'2 b4"))),
            15: SimpleSynchronousBars((SimpleBar("d''2 g''"), SimpleBar("c'4 c'4 b e'4"))),
            16: SimpleSynchronousBars((SimpleBar("g''8 [g'] g'' g'' g''2"), SimpleBar("c'4 b8 [a] b [c'] d' e'"))),
            17: SimpleSynchronousBars((SimpleBar("d''8 [d''] g'' fis'' g''2"), SimpleBar("c'4 b4 e'8 [d'] c' b"))),
            18: SimpleSynchronousBars((SimpleBar("g''4 g' g''2"), SimpleBar("c'8 [c'] b [a] c' [b] a g"))),
            19: SimpleSynchronousBars((SimpleBar("g''8 [a''] b'' c''' f''2"), SimpleBar("a2 d'8 c' b a"))),
            20: SimpleSynchronousBars((SimpleBar("g''4 c'' f''2"), SimpleBar("a2. b4"))),
            21: SimpleSynchronousBars((SimpleBar("g''8 [c''] d'' e'' f''4 f''"), SimpleBar("a4 bes a8 [c'] a f"))),
            22: SimpleSynchronousBars((SimpleBar("g''8 [c''] b' c'' f''2"), SimpleBar("a2 (a8) [b] c' d'"))),
            23: SimpleSynchronousBars((SimpleBar("g''8 [g''] c'''8 g'' f''4 f''4"), SimpleBar("a2 d8 [f] e d"))),
            24: SimpleSynchronousBars((SimpleBar("g''2 f''"), SimpleBar("a2. d'4"))),
            25: SimpleSynchronousBars((SimpleBar("g''8 [g''] f'' e'' f''2"), SimpleBar("a4 a (a8) [a] g f"))),
            26: SimpleSynchronousBars((SimpleBar("g''8 [e''] d'' c'' f''4 f''"), SimpleBar("a4 a2 d'4"))),
            27: SimpleSynchronousBars((SimpleBar("g''8 [c''] f'' e'' f''2"), SimpleBar("a2 (a8) [c'] b a"))),
            28: SimpleSynchronousBars((SimpleBar("f''4 f'' e''8 [c''] a'' c''"), SimpleBar("g4 a8 b c'2"))),
            29: SimpleSynchronousBars((SimpleBar("f''4 e''8 d'' e''4 c''"), SimpleBar("g2 c'4 c'"))),
            30: SimpleSynchronousBars((SimpleBar("f''8 [f''] e'' [d''] e'' [e''] d'' c''"), SimpleBar("g4 g4 c'2"))),
            31: SimpleSynchronousBars(
                (SimpleBar("f''4 e''8 [d''] e'' [g''] e'' c''"), SimpleBar("g8 [g] a b c'4 c'4"))),
            32: SimpleSynchronousBars((SimpleBar("f''4 f''4 (f''8) [e''] d'' c''"), SimpleBar("g8 [d'] c' b c'4 c'"))),
            33: SimpleSynchronousBars((SimpleBar("f''4. f''8 e'' [d''] e'' c''"), SimpleBar("g4 g c' c'"))),
            34: SimpleSynchronousBars((SimpleBar("f''4 f''2 e''4"), SimpleBar("g8 [g] c'8 b c'4 c'"))),
            35: SimpleSynchronousBars((SimpleBar("f''4 f'' e'' a''"), SimpleBar("g4 c'8 b c'2"))),
            36: SimpleSynchronousBars((SimpleBar("f''8 [b'] c'' [d''] e'' [g''] f'' e''"), SimpleBar("g2 c4 c'4"))),
            37: SimpleSynchronousBars((SimpleBar("d''2. c''8 d''"), SimpleBar("c'4 b8 a b2"))),
            38: SimpleSynchronousBars((SimpleBar("d''4 g''8 a'' g''4. f''8"), SimpleBar("c'4 b8 a b4 a8 b"))),
            39: SimpleSynchronousBars((SimpleBar("d''2 d''2"), SimpleBar("c'4 b4 (b8) a b4"))),
            40: SimpleSynchronousBars((SimpleBar("d''1"), SimpleBar("c'8 [a] b [c'] b [c'] a b"))),
            41: SimpleSynchronousBars((SimpleBar("d''4 g''2 f''8 g''8"), SimpleBar("c'4 c' b b"))),
            42: SimpleSynchronousBars((SimpleBar("d''4 d''8 [c''] d'' e'' f''4"), SimpleBar("c'4 b2 a8 b"))),
            43: SimpleSynchronousBars((SimpleBar("d''4 g'4 g'' f''"), SimpleBar("c'2 b2"))),
            44: SimpleSynchronousBars((SimpleBar("d''4 g'' g' f''"), SimpleBar("c'2 b4 a8 b"))),
            45: SimpleSynchronousBars(
                (SimpleBar("d''4 g''8 [a''] g'' [a''] f'' g''"), SimpleBar("c'8 [c'] b [a] b [b] a b"))),
            46: SimpleSynchronousBars((SimpleBar("e''8 [f''] d'' e'' c''2"), SimpleBar("c'1"))),
            47: SimpleSynchronousBars((SimpleBar("e''8 [f''] e'' d'' c''2"), SimpleBar("c'1"))),
            48: SimpleSynchronousBars((SimpleBar("e''4 d''8 e'' c''2"), SimpleBar("c'1"))),
            49: SimpleSynchronousBars((SimpleBar("e''8 [d''] e'' d'' c''2"), SimpleBar("c'1"))),
            50: SimpleSynchronousBars((SimpleBar("e''8 [f''] g'' e'' c''2"), SimpleBar("c'1"))),
            51: SimpleSynchronousBars((SimpleBar("e''8 [g''] e'' d'' c''2"), SimpleBar("c'1"))),
            52: SimpleSynchronousBars((SimpleBar("e''8 [c''] e'' d'' c''2"), SimpleBar("c'1"))),
            53: SimpleSynchronousBars((SimpleBar("e''4. d''8 c''2"), SimpleBar("c'1"))),
            54: SimpleSynchronousBars((SimpleBar("e''8 [c'''] g'' e'' c''2"), SimpleBar("c'1")))})
