__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from importlib import resources

import jinja2
import numpy as np

from musical_games.dice_games.base import (SimpleDiceTable, SimpleMidiSettings, SimpleDiceGame)
from musical_games.dice_games.data_csv import SimpleBarCollectionCSVReader


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
                                          / 'data/dice_games/cpe_bach_counterpoint/bars_treble.csv')
        bass_bars = csv_reader.read_csv(resources.files('musical_games')
                                        / 'data/dice_games/cpe_bach_counterpoint/bars_bass.csv')

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/cpe_bach_counterpoint/lilypond')
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
                                                         'data/dice_games/kirnberger_menuet_trio/menuet_bars.csv'),
                           'trio': csv_reader.read_csv(resources.files('musical_games') /
                                                       'data/dice_games/kirnberger_menuet_trio/trio_bars.csv')}

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/kirnberger_menuet_trio/lilypond')
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


class KirnbergerPolonaise(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Polonaise dice game by Kirnberger.

        This dice game has measures for a piano part and two violin parts.
        """
        dice_tables = {
            'polonaise': SimpleDiceTable(np.array([
                [70, 34, 68, 18, 32, 58, 80, 11, 59, 35, 74, 13, 21, 33],
                [10, 24, 50, 46, 14, 26, 22, 77, 65, 5, 27, 71, 15, 39],
                [42, 6, 60, 2, 52, 66, 82, 3, 9, 83, 67, 1, 53, 25],
                [62, 8, 36, 12, 16, 38, 43, 41, 45, 17, 37, 49, 73, 23],
                [44, 56, 40, 79, 48, 54, 78, 84, 29, 76, 61, 57, 51, 75],
                [72, 30, 4, 28, 22, 64, 69, 63, 7, 47, 19, 31, 81, 55],
                [114, 112, 126, 87, 89, 88, 90, 93, 86, 94, 96, 85, 95, 104],
                [123, 116, 137, 110, 91, 98, 129, 99, 107, 122, 105, 93, 106, 121],
                [131, 147, 143, 113, 101, 115, 103, 140, 111, 145, 133, 109, 117, 125],
                [138, 151, 118, 124, 141, 127, 142, 149, 97, 134, 120, 100, 119, 132],
                [144, 153, 146, 128, 150, 154, 152, 102, 135, 148, 136, 108, 130, 139]]))
        }

        csv_reader = SimpleBarCollectionCSVReader()
        bar_collections = {'polonaise': csv_reader.read_csv(resources.files('musical_games') /
                                                            'data/dice_games/kirnberger_polonaise/polonaise_bars.csv')}

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/kirnberger_polonaise/lilypond')
        env_options = self._standard_jinja2_environment_options() | {'loader': template_loader}
        jinja2_environment = jinja2.Environment(**env_options)

        midi_settings = SimpleMidiSettings(
            {'polonaise': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand',
                           'violin_1': 'Violin', 'violin_2': 'Violin'}},
            {'polonaise': {'piano_right_hand': 0, 'piano_left_hand': 0,
                           'violin_1': 0, 'violin_2': 0}},
            {'polonaise': {'piano_right_hand': 0.75, 'piano_left_hand': 0.6,
                           'violin_1': 0.8625, 'violin_2': 0.8625}})

        super().__init__('Kirnberger', 'Polonaise', dice_tables, bar_collections,
                         jinja2_environment, midi_settings)


class MozartWaltz(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Waltz dice game by Mozart."""
        dice_tables = {
            'waltz': SimpleDiceTable(np.array([
                [96, 22, 141, 41, 105, 122, 11, 30, 70, 121, 26, 9, 112, 49, 109, 14],
                [32, 6, 128, 63, 146, 46, 134, 81, 117, 39, 126, 56, 174, 18, 116, 83],
                [69, 95, 158, 13, 153, 55, 110, 24, 66, 139, 15, 132, 73, 58, 145, 79],
                [40, 17, 113, 85, 161, 2, 159, 100, 90, 176, 7, 34, 67, 160, 52, 170],
                [148, 74, 163, 45, 80, 97, 36, 107, 25, 143, 64, 125, 76, 136, 1, 93],
                [104, 157, 27, 167, 154, 68, 118, 91, 138, 71, 150, 29, 101, 162, 23, 151],
                [152, 60, 171, 53, 99, 133, 21, 127, 16, 155, 57, 175, 43, 168, 89, 172],
                [119, 84, 114, 50, 140, 86, 169, 94, 120, 88, 48, 166, 51, 115, 72, 111],
                [98, 142, 42, 156, 75, 129, 62, 123, 65, 77, 19, 82, 137, 38, 149, 8],
                [3, 87, 165, 61, 135, 47, 147, 33, 102, 4, 31, 164, 144, 59, 173, 78],
                [54, 130, 10, 103, 28, 37, 106, 5, 35, 20, 108, 92, 12, 124, 44, 131]]))
        }

        csv_reader = SimpleBarCollectionCSVReader()
        bar_collections = {'waltz': csv_reader.read_csv(resources.files('musical_games') /
                                                        'data/dice_games/mozart_waltz/waltz_bars.csv')}

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/mozart_waltz/lilypond')
        env_options = self._standard_jinja2_environment_options() | {'loader': template_loader}
        jinja2_environment = jinja2.Environment(**env_options)

        midi_settings = SimpleMidiSettings(
            {'waltz': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'waltz': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'waltz': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Mozart', 'Waltz', dice_tables, bar_collections,
                         jinja2_environment, midi_settings)


class StadlerMenuetTrio(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Menuet and Trio dice game by Stadler.

        A similar dice game has been made by Haydn.

        In this dice game, there is a dice table for the menuet and one for the trio.
        """
        dice_tables = {
            'menuet': SimpleDiceTable(np.array([
                [96, 22, 141, 41, 105, 122, 11, 30, 70, 121, 26, 9, 112, 49, 109, 14],
                [32, 6, 128, 63, 146, 46, 134, 81, 117, 39, 126, 56, 174, 18, 116, 83],
                [69, 95, 158, 13, 153, 55, 110, 24, 66, 139, 15, 132, 73, 58, 145, 79],
                [40, 17, 113, 85, 161, 2, 159, 100, 90, 176, 7, 34, 67, 160, 52, 170],
                [148, 74, 163, 45, 80, 97, 36, 107, 25, 143, 64, 125, 76, 136, 1, 93],
                [104, 157, 27, 167, 154, 68, 118, 91, 138, 71, 150, 29, 101, 162, 23, 151],
                [152, 60, 171, 53, 99, 133, 21, 127, 16, 155, 57, 175, 43, 168, 89, 172],
                [119, 84, 114, 50, 140, 86, 169, 94, 120, 88, 48, 166, 51, 115, 72, 111],
                [98, 142, 42, 156, 75, 129, 62, 123, 65, 77, 19, 82, 137, 38, 149, 8],
                [3, 87, 165, 61, 135, 47, 147, 33, 102, 4, 31, 164, 144, 59, 173, 78],
                [54, 130, 10, 103, 28, 37, 106, 5, 35, 20, 108, 92, 12, 124, 44, 131]])),
            'trio': SimpleDiceTable(np.array([
                [72, 6, 59, 25, 81, 41, 89, 13, 36, 5, 46, 79, 30, 95, 19, 66],
                [56, 82, 42, 74, 14, 7, 26, 71, 76, 20, 64, 84, 8, 35, 47, 88],
                [75, 39, 54, 1, 65, 43, 15, 80, 9, 34, 93, 48, 69, 58, 90, 21],
                [40, 73, 16, 68, 29, 55, 2, 61, 22, 67, 49, 77, 57, 87, 33, 10],
                [83, 3, 28, 53, 37, 17, 44, 70, 63, 85, 32, 96, 12, 23, 50, 91],
                [18, 45, 62, 38, 4, 27, 52, 94, 11, 92, 24, 86, 51, 60, 78, 31]])),
        }

        csv_reader = SimpleBarCollectionCSVReader()
        bar_collections = {'menuet': csv_reader.read_csv(resources.files('musical_games') /
                                                         'data/dice_games/stadler_menuet_trio/menuet_bars.csv'),
                           'trio': csv_reader.read_csv(resources.files('musical_games') /
                                                       'data/dice_games/stadler_menuet_trio/trio_bars.csv')}

        template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/stadler_menuet_trio/lilypond')
        env_options = self._standard_jinja2_environment_options() | {'loader': template_loader}
        jinja2_environment = jinja2.Environment(**env_options)

        midi_settings = SimpleMidiSettings(
            {'menuet': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'},
             'trio': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'menuet': {'piano_right_hand': 0, 'piano_left_hand': 0},
             'trio': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'menuet': {'piano_right_hand': 1, 'piano_left_hand': 0.75},
             'trio': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Stadler', 'Menuet and Trio', dice_tables, bar_collections,
                         jinja2_environment, midi_settings)
