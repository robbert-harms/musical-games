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
                                            str_dice_table_name, int_bar_index, str_staff_name, SimpleDiceGame)
from musical_games.dice_games2.data_csv import SimpleBarCollectionCSVReader


class CPEBachCounterpoint(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Counterpoint dice by C.P.E. Bach.

        In this dice game, the right hand and left hand of the piano piece are shuffled independently by two
        dice tables.
        """
        dice_tables = {
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

        csv_reader = SimpleBarCollectionCSVReader()
        treble_bars = csv_reader.read_csv(resources.files('musical_games')
                                          / 'data/dice_games2/cpe_bach_counterpoint/bars_treble.csv')
        bass_bars = csv_reader.read_csv(resources.files('musical_games')
                                        / 'data/dice_games2/cpe_bach_counterpoint/bars_bass.csv')

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games2/cpe_bach_counterpoint/lilypond')
        env_options = self._standard_jinja2_environment_options() | {'loader': template_loader}
        jinja2_environment = jinja2.Environment(**env_options)

        midi_settings = SimpleMidiSettings(
            {'treble': {'piano_right_hand': 'acoustic grand'}, 'bass': {'piano_right_hand': 'acoustic grand'}},
            {'treble': {'piano_right_hand': 0}, 'bass': {'piano_right_hand': 0}},
            {'treble': {'piano_right_hand': 1}, 'bass': {'piano_right_hand': 0.75}})

        super().__init__('C.P.E. Bach', 'Counterpoint', dice_tables, {'treble': treble_bars, 'bass': bass_bars},
                         jinja2_environment, midi_settings)
        self._table_name_to_staff_name: dict[str_dice_table_name, str_staff_name] = {'treble': 'treble', 'bass': 'bass'}

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
