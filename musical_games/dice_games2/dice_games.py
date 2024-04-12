__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from importlib import resources

import jinja2
import numpy as np

from musical_games.dice_games2.base import (SimpleDiceTable, SimpleMidiSettings,
                                            str_dice_table_name, str_staff_name, SimpleDiceGame)
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
            {'treble': {'piano_right_hand': 'acoustic grand'}, 'bass': {'piano_left_hand': 'acoustic grand'}},
            {'treble': {'piano_right_hand': 0}, 'bass': {'piano_left_hand': 0}},
            {'treble': {'piano_right_hand': 1}, 'bass': {'piano_left_hand': 0.75}})

        super().__init__('C.P.E. Bach', 'Counterpoint', dice_tables, {'treble': treble_bars, 'bass': bass_bars},
                         jinja2_environment, midi_settings)



class KirnbergerMenuetTrio(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Menuet and Trio dice game by Kirnberger.

        In this dice game, there is a dice table for the menuet and one for the trio.
        """
        dice_tables = {
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

        csv_reader = SimpleBarCollectionCSVReader()
        bar_collections = {'menuet': csv_reader.read_csv(resources.files('musical_games') /
                                                         'data/dice_games2/kirnberger_menuet_trio/menuet_bars.csv'),
                           'trio': csv_reader.read_csv(resources.files('musical_games') /
                                                       'data/dice_games2/kirnberger_menuet_trio/trio_bars.csv')}

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games2/kirnberger_menuet_trio/lilypond')
        env_options = self._standard_jinja2_environment_options() | {'loader': template_loader}
        jinja2_environment = jinja2.Environment(**env_options)

        midi_settings = SimpleMidiSettings(
            {'menuet': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'},
             'trio': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'menuet': {'piano_right_hand': 0, 'piano_left_hand': 0},
             'trio': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'menuet': {'piano_right_hand': 1, 'piano_left_hand': 0.75},
             'trio': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Kirnberger', 'Menuet and Trio', dice_tables, bar_collections,
                         jinja2_environment, midi_settings)
