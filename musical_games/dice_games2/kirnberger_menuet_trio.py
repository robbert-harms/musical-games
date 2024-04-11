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
                                            str_dice_table_key, int_bar_index)
from musical_games.dice_games2.data_csv import SimpleBarCollectionCSVReader


class KirnbergerMenuetTrio(DiceGame):

    def __init__(self):
        """Implementation of a Menuet and Trio dice game by Kirnberger.

        In this dice game, there is a dice table for the menuet and one for the trio.
        """
        self._author = 'Kirnberger'
        self._title = 'Menuet and Trio'
        self._dice_tables = {
            'menuet': SimpleDiceTable(np.array([
                [23, 77, 62, 70, 29, 83, 59, 36, 33, 60, 21, 14, 45, 68, 26, 40],
                [63, 54, 2, 53, 41, 37, 71, 90, 55, 46, 88, 39, 65, 6, 91, 81],
                [79, 75, 42, 5, 50, 69, 52, 8, 4, 12, 94, 9, 25, 35, 66, 24],
                [13, 57, 64, 74, 11, 3, 67, 73, 95, 78, 80, 30, 1, 51, 82, 16],
                [43, 7, 86, 31, 18, 89, 87, 58, 38, 93, 15, 92, 28, 61, 72, 85],
                [32, 47, 84, 20, 22, 49, 56, 48, 44, 76, 34, 19, 17, 10, 27, 96]])),
            'trio': SimpleDiceTable(np.array([
                [81, 57, 67, 2, 90, 41, 24, 56, 94, 47, 62, 72, 25, 64, 48, 87],
                [78, 45, 30, 65, 14, 33, 10, 73, 40, 55, 46, 17, 31, 85, 11, 76],
                [8, 69, 26, 53, 43, 95, 88, 63, 79, 5, 3, 60, 54, 21, 42, 82],
                [84, 6, 4, 22, 51, 12, 83, 92, 58, 93, 66, 23, 15, 13, 27, 32],
                [39, 28, 18, 35, 89, 75, 61, 96, 7, 91, 70, 1, 74, 44, 52, 50],
                [59, 71, 37, 16, 86, 49, 77, 20, 38, 68, 19, 29, 80, 36, 34, 9]])),
        }
        self._bar_collection = self._get_bar_collection()
    #     self._table_key_to_staff = {'treble': 0, 'bass': 1}
    #
    #     self._jinja2_environment_options = dict(
    #         block_start_string=r'\BLOCK{',
    #         block_end_string='}',
    #         variable_start_string=r'\VAR{',
    #         variable_end_string='}',
    #         comment_start_string=r'\#{',
    #         comment_end_string='}',
    #         line_statement_prefix='%-',
    #         line_comment_prefix='%#',
    #         trim_blocks=True,
    #         autoescape=False,
    #         lstrip_blocks=True
    #     )
    #     template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games2/cpe_bach_counterpoint/lilypond')
    #     env_options = self._jinja2_environment_options | {'loader': template_loader}
    #     self._jinja2_env = jinja2.Environment(**env_options)
    #
    @property
    def author(self) -> str:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    def get_dice_tables(self) -> dict[str, DiceTable]:
        return self._dice_tables

    def get_all_duplicate_bars(self, table_key: str_dice_table_key) -> list[set[int_bar_index]]:
        pass

    def count_unique_compositions(self, count_duplicates=False) -> int:
        pass

    def get_nmr_staffs_per_table(self) -> dict[str, int]:
        pass

    def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
        pass

    def get_default_midi_settings(self) -> MidiSettings:
        pass

    def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
        pass

    def compile_single_bar(self, table_key: str_dice_table_key, bar_ind: int_bar_index) -> LilypondScore:
        pass

    def compile_composition_score(self, bar_selection: BarSelection, comment: str | None = None) -> LilypondScore:
        pass

    def compile_composition_audio(self, bar_selection: BarSelection,
                                  midi_settings: MidiSettings | None = None) -> LilypondScore:
        pass

    # def get_all_duplicate_bars(self, table_key: str) -> list[set[int]]:
    #     bars = self._bar_collection.get_bars(self._table_key_to_staff[table_key])
    #
    #     bars_by_lilypond = {}
    #     for bar_ind, bar in bars.items():
    #         bar_indices = bars_by_lilypond.setdefault(bar.lilypond_str, set())
    #         bar_indices.add(bar_ind)
    #
    #     return [v for k, v in bars_by_lilypond.items() if len(v) > 1]
    #
    # def count_unique_compositions(self, count_duplicates=False) -> int:
    #     def count_unique_bars(table_key: str, bar_numbers: list[int]):
    #         """Count the number of unique bars in the provided list of bar numbers."""
    #         bars_of_table = self._bar_collection.get_bars(self._table_key_to_staff[table_key])
    #         bars = [bars_of_table[bar_number].lilypond_str for bar_number in bar_numbers]
    #         return len(set(bars))
    #
    #     table_counts = []
    #     for table_key, table in self._dice_tables.items():
    #         if count_duplicates:
    #             table_counts.append(table.max_dice_value ** table.nmr_throws)
    #         else:
    #             table_counts.append(reduce(mul, [count_unique_bars(table_key, column)
    #                                              for column in table.list_columns()]))
    #     return reduce(mul, table_counts)
    #
    # def get_nmr_staffs_per_table(self) -> dict[str, int]:
    #     return {k: 1 for k in self._dice_tables}
    #
    # def get_random_bar_selection(self, shuffle_staffs: bool = False, seed: int = None) -> BarSelection:
    #     choices = {}
    #     for table_key, dice_table in self._dice_tables.items():
    #         choices[table_key] = dice_table.get_random_selection(seed)
    #     return GroupedStaffsBarSelection(choices)
    #
    # def get_default_midi_settings(self) -> MidiSettings:
    #     return SimpleMidiSettings(
    #         {'treble': {0: 'acoustic grand', 1: 'test'}, 'bass': {0: 'acoustic grand'}},
    #         {'treble': {0: 0}, 'bass': {0: 0}},
    #         {'treble': {0: 1}, 'bass': {0: 0.75}})
    #
    # def compile_bars_overview(self, single_page: bool = False) -> LilypondScore:
    #     template = self._jinja2_env.get_template('bar_overview.ly')
    #     return SimpleLilypondScore(template.render(bar_collection=self._bar_collection,
    #                                                render_settings={'single_page': single_page}))
    #
    # def compile_single_bar(self, table_key: str, bar_ind: int) -> LilypondScore:
    #     template = self._jinja2_env.get_template('single_bar.ly')
    #     bar = self._bar_collection.get_bars(self._table_key_to_staff[table_key])[bar_ind]
    #     return SimpleLilypondScore(template.render(clef=table_key, bar=bar))
    #
    # def compile_composition_score(self, bar_selection: BarSelection, comment: str | None = None) -> LilypondScore:
    #     template = self._jinja2_env.get_template('composition_pdf.ly')
    #     return SimpleLilypondScore(template.render(composition_bars=self._bar_selection_to_bars(bar_selection),
    #                                                render_settings={'comment': comment}))
    #
    # def compile_composition_audio(self, bar_selection: BarSelection,
    #                               midi_settings: MidiSettings | None = None) -> LilypondScore:
    #     midi_settings = midi_settings or self.get_default_midi_settings()
    #     template = self._jinja2_env.get_template('composition_midi.ly')
    #     return SimpleLilypondScore(template.render(composition_bars=self._bar_selection_to_bars(bar_selection),
    #                                                midi_settings=midi_settings))
    #
    # def _bar_selection_to_bars(self, bar_selection: BarSelection) -> dict:
    #     """Transform a bar selection (containing indices) to the actual selection of bars.
    #
    #     The bar selection contains per dice table, and optionally per staff, the bar indices we want to use in a
    #     composition. This function should select from the collection of bars hold in this dice game the bars
    #     corresponding to the bar indices in the bar selection.
    #
    #     Args:
    #         bar_selection: the selected bar indices contained in a bar selection
    #
    #     Returns:
    #         A dictionary of any form, as usable by the composition templates in this dice game.
    #     """
    #     composition_bars = {
    #         'treble': [],
    #         'bass': []
    #     }
    #     for table_key in self._dice_tables.keys():
    #         for throw_ind in range(self._dice_tables[table_key].nmr_throws):
    #             bar_ind = bar_selection.get_bar_index(table_key, throw_ind)
    #             bar = self._bar_collection.get_bar(self._table_key_to_staff[table_key], bar_ind)
    #             composition_bars[table_key].append(bar)
    #     return composition_bars
    #
    # @staticmethod
    # def _get_bar_collection() -> BarCollection:
    #     """Get the collection of bars for this dice game.
    #
    #     Returns:
    #         The bars for this dice game as a synchronous bar collection. The first element of each synchronous bar
    #         is for the treble and the first dice table, the second is for the bass and the second dice table.
    #     """
    #     csv_reader = SimpleBarCollectionCSVReader()
    #     return csv_reader.read_csv(resources.files('musical_games') / 'data/dice_games2/cpe_bach_counterpoint/bars.csv')
