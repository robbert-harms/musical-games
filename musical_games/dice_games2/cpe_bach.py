__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from importlib import resources
from functools import reduce
from operator import mul

import jinja2
import numpy as np

from musical_games.dice_games2.base import (DiceGame, SimpleDiceTable, SimpleLilypondScore, LilypondScore,
                                            DiceTable, BarCollection, BarSelection, \
                                            GroupedStaffsBarSelection, MidiSettings, SimpleMidiSettings,
                                            str_dice_table_name, int_bar_index, str_staff_name)
from musical_games.dice_games2.data_csv import SimpleBarCollectionCSVReader


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
        self._table_name_to_staff_name: dict[str_dice_table_name, str_staff_name] = {'treble': 'treble', 'bass': 'bass'}

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

    def get_dice_tables(self) -> dict[str_dice_table_name, DiceTable]:
        return self._dice_tables

    def get_all_duplicate_bars(self, table_name: str_dice_table_name) -> list[set[int_bar_index]]:
        bars = self._bar_collection.get_bars(self._table_name_to_staff_name[table_name])

        bars_by_lilypond = {}
        for bar_ind, bar in bars.items():
            bar_indices = bars_by_lilypond.setdefault(bar.lilypond_str, set())
            bar_indices.add(bar_ind)

        return [v for k, v in bars_by_lilypond.items() if len(v) > 1]

    def count_unique_compositions(self, count_duplicates=False) -> int:
        def count_unique_bars(table_name: str, bar_numbers: list[int]):
            """Count the number of unique bars in the provided list of bar numbers."""
            bars_of_table = self._bar_collection.get_bars(self._table_name_to_staff_name[table_name])
            bars = [bars_of_table[bar_number].lilypond_str for bar_number in bar_numbers]
            return len(set(bars))

        table_counts = []
        for table_name, table in self._dice_tables.items():
            if count_duplicates:
                table_counts.append(table.max_dice_value ** table.nmr_throws)
            else:
                table_counts.append(reduce(mul, [count_unique_bars(table_name, column)
                                                 for column in table.list_columns()]))
        return reduce(mul, table_counts)

    def get_nmr_staffs_per_table(self) -> dict[str, int]:
        return {k: 1 for k in self._dice_tables}

    def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
        choices = {}
        for table_name, dice_table in self._dice_tables.items():
            choices[table_name] = dice_table.get_random_selection(seed)
        return GroupedStaffsBarSelection(choices)

    def get_default_midi_settings(self) -> MidiSettings:
        return SimpleMidiSettings(
            {'treble': {'treble': 'acoustic grand'}, 'bass': {'bass': 'acoustic grand'}},
            {'treble': {'treble': 0}, 'bass': {'bass': 0}},
            {'treble': {'treble': 1}, 'bass': {'bass': 0.75}})

    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        template = self._jinja2_env.get_template('bar_overview.ly')
        return SimpleLilypondScore(template.render(bar_collection=self._bar_collection,
                                                   render_settings={'single_page': single_page}))

    def compile_single_bar(self, table_name: str_dice_table_name, bar_ind: int_bar_index) -> LilypondScore:
        template = self._jinja2_env.get_template('single_bar.ly')
        bar = self._bar_collection.get_bars(self._table_name_to_staff_name[table_name])[bar_ind]
        return SimpleLilypondScore(template.render(clef=self._table_name_to_staff_name[table_name], bar=bar))

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
                bar = self._bar_collection.get_bar(self._table_name_to_staff_name[table_key], bar_ind)
                composition_bars[table_key].append(bar)
        return composition_bars

    @staticmethod
    def _get_bar_collection() -> BarCollection:
        """Get the collection of bars for this dice game.

        Returns:
            The bars for this dice game as a synchronous bar collection. The first element of each synchronous bar
            is for the treble and the first dice table, the second is for the bass and the second dice table.
        """
        csv_reader = SimpleBarCollectionCSVReader()
        return csv_reader.read_csv(resources.files('musical_games') / 'data/dice_games2/cpe_bach_counterpoint/bars.csv')
