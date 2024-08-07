__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import json
import re
from dataclasses import dataclass
from importlib import resources

from musical_games.dice_games.base import (SimpleDiceTable, SimpleMidiSettings, SimpleDiceGame, BarAnnotation)
from musical_games.dice_games.data_csv import CSVBarCollectionLoader, AnnotationLoader


class CPEBachCounterpoint(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Counterpoint dice by C.P.E. Bach.

        In this dice game, the right hand and left hand of the piano piece are shuffled independently by two
        dice tables.
        """
        dice_tables = {
            'treble': SimpleDiceTable.from_lists([
                [1, 10, 19, 28, 37, 46],
                [2, 11, 20, 29, 38, 47],
                [3, 12, 21, 30, 39, 48],
                [4, 13, 22, 31, 40, 49],
                [5, 14, 23, 32, 41, 50],
                [6, 15, 24, 33, 42, 51],
                [7, 16, 25, 34, 43, 52],
                [8, 17, 26, 35, 44, 53],
                [9, 18, 27, 36, 45, 54]]),
            'bass': SimpleDiceTable.from_lists([
                [1, 10, 19, 28, 37, 46],
                [2, 11, 20, 29, 38, 47],
                [3, 12, 21, 30, 39, 48],
                [4, 13, 22, 31, 40, 49],
                [5, 14, 23, 32, 41, 50],
                [6, 15, 24, 33, 42, 51],
                [7, 16, 25, 34, 43, 52],
                [8, 17, 26, 35, 44, 53],
                [9, 18, 27, 36, 45, 54]]),
        }
        data_name = 'cpe_bach_counterpoint'

        treble_bars = CSVBarCollectionLoader(resources.files('musical_games')
                                             / f'data/dice_games/{data_name}/bars_treble.csv').load_data()
        bass_bars = CSVBarCollectionLoader(resources.files('musical_games')
                                           / f'data/dice_games/{data_name}/bars_bass.csv').load_data()

        midi_settings = SimpleMidiSettings(
            {'treble': {'piano_right_hand': 'acoustic grand'}, 'bass': {'piano_left_hand': 'acoustic grand'}},
            {'treble': {'piano_right_hand': 0}, 'bass': {'piano_left_hand': 0}},
            {'treble': {'piano_right_hand': 1}, 'bass': {'piano_left_hand': 0.75}})

        super().__init__('C.P.E. Bach', 'Counterpoint', dice_tables, {'treble': treble_bars, 'bass': bass_bars},
                         self._generate_jinja2_environment(data_name), midi_settings)


class KirnbergerMenuetTrio(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Menuet and Trio dice game by Kirnberger.

        In this dice game, there is a dice table for the menuet and one for the trio.
        """
        dice_tables = {
            'menuet': SimpleDiceTable.from_lists([
                [23, 77, 62, 70, 29, 83, 59, 36, 33, 60, 21, 14, 45, 68, 26, 40],
                [63, 54, 2, 53, 41, 37, 71, 90, 55, 46, 88, 39, 65, 6, 91, 81],
                [79, 75, 42, 5, 50, 69, 52, 8, 4, 12, 94, 9, 25, 35, 66, 24],
                [13, 57, 64, 74, 11, 3, 67, 73, 95, 78, 80, 30, 1, 51, 82, 16],
                [43, 7, 86, 31, 18, 89, 87, 58, 38, 93, 15, 92, 28, 61, 72, 85],
                [32, 47, 84, 20, 22, 49, 56, 48, 44, 76, 34, 19, 17, 10, 27, 96]]),
            'trio': SimpleDiceTable.from_lists([
                [81, 57, 67, 2, 90, 41, 24, 56, 94, 47, 62, 72, 25, 64, 48, 87],
                [78, 45, 30, 65, 14, 33, 10, 73, 40, 55, 46, 17, 31, 85, 11, 76],
                [8, 69, 26, 53, 43, 95, 88, 63, 79, 5, 3, 60, 54, 21, 42, 82],
                [84, 6, 4, 22, 51, 12, 83, 92, 58, 93, 66, 23, 15, 13, 27, 32],
                [39, 28, 18, 35, 89, 75, 61, 96, 7, 91, 70, 1, 74, 44, 52, 50],
                [59, 71, 37, 16, 86, 49, 77, 20, 38, 68, 19, 29, 80, 36, 34, 9]]),
        }
        data_name = 'kirnberger_menuet_trio'

        bar_collections = {'menuet': CSVBarCollectionLoader(resources.files('musical_games') /
                                                            f'data/dice_games/{data_name}/menuet_bars.csv').load_data(),
                           'trio': CSVBarCollectionLoader(resources.files('musical_games') /
                                                          f'data/dice_games/{data_name}/trio_bars.csv').load_data()}

        midi_settings = SimpleMidiSettings(
            {'menuet': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'},
             'trio': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'menuet': {'piano_right_hand': 0, 'piano_left_hand': 0},
             'trio': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'menuet': {'piano_right_hand': 1, 'piano_left_hand': 0.75},
             'trio': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Kirnberger', 'Menuet and Trio', dice_tables, bar_collections,
                         self._generate_jinja2_environment(data_name), midi_settings)


class KirnbergerPolonaise(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Polonaise dice game by Kirnberger.

        This dice game has measures for a piano part and two violin parts.
        """
        dice_tables = {
            'polonaise': SimpleDiceTable.from_lists([
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
                [144, 153, 146, 128, 150, 154, 152, 102, 135, 148, 136, 108, 130, 139]])
        }
        data_name = 'kirnberger_polonaise'

        bar_collections = {
            'polonaise': CSVBarCollectionLoader(resources.files('musical_games') /
                                                f'data/dice_games/{data_name}/polonaise_bars.csv').load_data()
        }

        midi_settings = SimpleMidiSettings(
            {'polonaise': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand',
                           'violin_1': 'Violin', 'violin_2': 'Violin'}},
            {'polonaise': {'piano_right_hand': 0, 'piano_left_hand': 0,
                           'violin_1': 0, 'violin_2': 0}},
            {'polonaise': {'piano_right_hand': 0.75, 'piano_left_hand': 0.6,
                           'violin_1': 0.8625, 'violin_2': 0.8625}})

        super().__init__('Kirnberger', 'Polonaise', dice_tables, bar_collections,
                         self._generate_jinja2_environment(data_name), midi_settings)


class MozartContredanse(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Contredanse dice game by Mozart."""
        dice_tables = {
            'contredanse': SimpleDiceTable.from_lists([
                [70, 14, 164, 122, 25, 153, 18, 167, 155, 3, 162, 170, 13, 166, 95, 5],
                [10, 64, 100, 12, 149, 30, 161, 11, 148, 28, 135, 173, 169, 174, 2, 20],
                [33, 1, 160, 163, 77, 156, 168, 172, 22, 176, 62, 126, 31, 24, 159, 41],
                [36, 114, 8, 35, 111, 39, 137, 44, 4, 157, 38, 9, 151, 32, 17, 171],
                [105, 150, 57, 71, 117, 52, 132, 130, 136, 91, 138, 19, 134, 101, 154, 146],
                [165, 152, 112, 15, 147, 27, 73, 102, 144, 104, 87, 107, 128, 48, 109, 74],
                [7, 81, 131, 37, 21, 125, 49, 115, 116, 133, 72, 141, 94, 80, 129, 65],
                [142, 106, 40, 69, 43, 140, 23, 89, 66, 124, 26, 84, 75, 103, 96, 127],
                [99, 68, 86, 139, 120, 92, 143, 83, 93, 55, 29, 51, 42, 110, 108, 98],
                [85, 45, 90, 158, 82, 123, 78, 58, 61, 34, 119, 46, 59, 54, 60, 47],
                [145, 97, 6, 121, 56, 67, 63, 16, 50, 79, 175, 76, 113, 88, 53, 118]])
        }
        data_name = 'mozart_contredanse'

        bar_collections = {
            'contredanse': CSVBarCollectionLoader(resources.files('musical_games') /
                                                  f'data/dice_games/{data_name}/contredanse_bars.csv').load_data()
        }

        midi_settings = SimpleMidiSettings(
            {'contredanse': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'contredanse': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'contredanse': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        def split_voices(voices):
            return re.findall(r'<<{\\voiceOne ([^}]*)} \\new Voice {\\voiceTwo ([^}]*)}>>', voices)[0]

        jinja2_env = self._generate_jinja2_environment(data_name)
        jinja2_env.globals['split_voices'] = split_voices

        super().__init__('Mozart', 'Contredanse', dice_tables, bar_collections,
                         jinja2_env, midi_settings)


class MozartWaltz(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Waltz dice game by Mozart."""
        dice_tables = {
            'waltz': SimpleDiceTable.from_lists([
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
                [54, 130, 10, 103, 28, 37, 106, 5, 35, 20, 108, 92, 12, 124, 44, 131]])
        }
        data_name = 'mozart_waltz'

        bar_collections = {'waltz': CSVBarCollectionLoader(resources.files('musical_games') /
                                                           f'data/dice_games/{data_name}/waltz_bars.csv').load_data()}

        midi_settings = SimpleMidiSettings(
            {'waltz': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'waltz': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'waltz': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        def split_voices(voices):
            return re.findall(r'<<{\\voiceOne ([^}]*)} \\new Voice {\\voiceTwo ([^}]*)}>>', voices)[0]

        jinja2_env = self._generate_jinja2_environment(data_name)
        jinja2_env.globals['split_voices'] = split_voices

        super().__init__('Mozart', 'Waltz', dice_tables, bar_collections,
                         jinja2_env, midi_settings)


class StadlerMenuetTrio(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Menuet and Trio dice game by Stadler.

        A similar dice game has been made by Haydn.

        In this dice game, there is a dice table for the menuet and one for the trio.
        """
        dice_tables = {
            'menuet': SimpleDiceTable.from_lists([
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
                [54, 130, 10, 103, 28, 37, 106, 5, 35, 20, 108, 92, 12, 124, 44, 131]]),
            'trio': SimpleDiceTable.from_lists([
                [72, 6, 59, 25, 81, 41, 89, 13, 36, 5, 46, 79, 30, 95, 19, 66],
                [56, 82, 42, 74, 14, 7, 26, 71, 76, 20, 64, 84, 8, 35, 47, 88],
                [75, 39, 54, 1, 65, 43, 15, 80, 9, 34, 93, 48, 69, 58, 90, 21],
                [40, 73, 16, 68, 29, 55, 2, 61, 22, 67, 49, 77, 57, 87, 33, 10],
                [83, 3, 28, 53, 37, 17, 44, 70, 63, 85, 32, 96, 12, 23, 50, 91],
                [18, 45, 62, 38, 4, 27, 52, 94, 11, 92, 24, 86, 51, 60, 78, 31]]),
        }
        data_name = 'stadler_menuet_trio'

        bar_collections = {'menuet': CSVBarCollectionLoader(resources.files('musical_games') /
                                                            f'data/dice_games/{data_name}/menuet_bars.csv').load_data(),
                           'trio': CSVBarCollectionLoader(resources.files('musical_games') /
                                                          f'data/dice_games/{data_name}/trio_bars.csv').load_data()}

        midi_settings = SimpleMidiSettings(
            {'menuet': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'},
             'trio': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'menuet': {'piano_right_hand': 0, 'piano_left_hand': 0},
             'trio': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'menuet': {'piano_right_hand': 1, 'piano_left_hand': 0.75},
             'trio': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Stadler', 'Menuet and Trio', dice_tables, bar_collections,
                         self._generate_jinja2_environment(data_name), midi_settings)


class GerlachScottishDance(SimpleDiceGame):

    def __init__(self):
        """Implementation of a Scottish dance dice game by Gerlach."""
        dice_tables = {
            'dance': SimpleDiceTable.from_lists([
                [(65, 14), (29, 17), (108, 96), (37, 50), (41, 35), (92, 139), (49, 90), (11, 59)],
                [(77, 109), (9, 28), (48, 99), (21, 7), (6, 80), (1, 47), (107, 31), (127, 51)],
                [(15, 87), (55, 95), (144, 74), (104, 120), (130, 100), (71, 150), (111, 69), (72, 102)],
                [(89, 12), (75, 3), (66, 175), (20, 70), (149, 46), (117, 94), (19, 86), (128, 52)],
                [(40, 98), (36, 10), (78, 44), (33, 136), (39, 110), (143, 30), (58, 67), (22, 91)],
                [(8, 88), (101, 32), (60, 4), (106, 93), (105, 45), (112, 27), (61, 119), (103, 148)]]),
            'trio': SimpleDiceTable.from_lists([
                [(13, 85), (126, 180), (125, 68), (177, 192), (187, 63), (24, 97), (145, 185), (137, 176)],
                [(165, 113), (23, 76), (82, 2), (154, 190), (5, 84), (161, 182), (174, 116), (54, 124)],
                [(43, 57), (135, 188), (56, 18), (189, 163), (25, 38), (166, 122), (179, 123), (169, 53)],
                [(181, 129), (131, 186), (115, 170), (62, 178), (183, 132), (168, 171), (81, 151), (158, 64)],
                [(134, 26), (118, 184), (160, 140), (114, 34), (42, 164), (146, 83), (141, 162), (73, 153)],
                [(79, 191), (121, 155), (138, 156), (16, 173), (133, 167), (142, 172), (147, 159), (152, 157)]]),
        }
        data_name = 'gerlach_scottish_dance'

        csv_reader = CSVBarCollectionLoader(
            resources.files('musical_games') / f'data/dice_games/{data_name}/scottish_dance_bars.csv',
            annotation_data_csv=resources.files('musical_games') /
                                f'data/dice_games/{data_name}/scottish_dance_bars_annotations.csv',
            annotation_loader=GerlachScottishDance.GerlachAnnotationLoader()
        )
        bars = csv_reader.load_data()

        bar_collections = {'dance': bars,
                           'trio': bars}

        midi_settings = SimpleMidiSettings(
            {'dance': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'},
             'trio': {'piano_right_hand': 'acoustic grand', 'piano_left_hand': 'acoustic grand'}},
            {'dance': {'piano_right_hand': 0, 'piano_left_hand': 0},
             'trio': {'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'dance': {'piano_right_hand': 1, 'piano_left_hand': 0.75},
             'trio': {'piano_right_hand': 1, 'piano_left_hand': 0.75}})

        super().__init__('Gerlach', 'Scottish dance', dice_tables, bar_collections,
                         self._generate_jinja2_environment(data_name), midi_settings)

    @dataclass(frozen=True, slots=True)
    class GerlachAnnotation(BarAnnotation):
        """Annotation for a bar in the Gerlach dice game.

        The only annotation is the presence of a clef change at the beginning of a bar.

        Args:
            has_clef_change: if the annotated bar has a clef change at the beginning
            clef: a string literal if there is a clef change at the beginning of this bar
        """
        has_clef_change: bool
        clef: str | None

    class GerlachAnnotationLoader(AnnotationLoader):

        def load_annotation(self, input_data: str) -> BarAnnotation:
            if input_data == '':
                return GerlachScottishDance.GerlachAnnotation(False, None)
            else:
                return GerlachScottishDance.GerlachAnnotation(True, json.loads(input_data)['clef'])


class CalegariAria(SimpleDiceGame):

    def __init__(self):
        """Implementation of an Aria by Calegari."""
        dice_tables = {
            'part_one': SimpleDiceTable.from_lists([
                [150, 142, 18, 85, 62, 3, 152, 94],
                [71, 89, 149, 137, 113, 56, 5, 132],
                [81, 13, 111, 10, 96, 154, 27, 179],
                [140, 184, 55, 2, 9, 175, 73, 90],
                [180, 34, 59, 98, 141, 166, 78, 143],
                [122, 127, 174, 192, 24, 46, 107, 183],
                [82, 15, 112, 58, 133, 118, 16, 105],
                [43, 38, 136, 116, 170, 193, 129, 92],
                [44, 181, 39, 109, 29, 63, 197, 172],
                [160, 48, 73, 182, 80, 42, 138, 4],
                [104, 68, 114, 47, 124, 86, 52, 162]]),
            'part_two': SimpleDiceTable.from_lists([
                [25, 120, 187, 102, 33, 157, 189, 108, 146, 148],
                [19, 171, 88, 28, 126, 35, 65, 64, 20, 61],
                [178, 99, 185, 97, 23, 147, 50, 117, 125, 159],
                [176, 17, 95, 195, 163, 6, 131, 144, 53, 169],
                [30, 177, 101, 11, 32, 165, 26, 123, 190, 69],
                [135, 134, 151, 54, 115, 36, 1, 60, 103, 45],
                [161, 153, 87, 41, 188, 155, 194, 198, 77, 164],
                [130, 37, 139, 57, 67, 168, 83, 75, 70, 119],
                [49, 173, 128, 79, 156, 51, 84, 8, 167, 14],
                [40, 12, 121, 158, 91, 110, 31, 66, 100, 22],
                [186, 21, 191, 76, 145, 74, 93, 106, 196, 7],
            ]),
        }
        data_name = 'calegari_aria'

        bars = CSVBarCollectionLoader(resources.files('musical_games') /
                               f'data/dice_games/{data_name}/bars_aria.csv').load_data()

        bar_collections = {
            'part_one': bars,
            'part_two': bars}

        midi_settings = SimpleMidiSettings(
            {'part_one': {'chant': 'Choir Aahs',
                          'piano_right_hand': 'acoustic grand',
                          'piano_left_hand': 'acoustic grand'},
             'part_two': {'chant': 'Choir Aahs',
                          'piano_right_hand': 'acoustic grand',
                          'piano_left_hand': 'acoustic grand'}},
            {'part_one': {'chant': 0, 'piano_right_hand': 0, 'piano_left_hand': 0},
             'part_two': {'chant': 0, 'piano_right_hand': 0, 'piano_left_hand': 0}},
            {'part_one': {'chant': 1, 'piano_right_hand': 0.9, 'piano_left_hand': 0.8},
             'part_two': {'chant': 1, 'piano_right_hand': 0.9, 'piano_left_hand': 0.8}})

        super().__init__('Calegari', 'Aria', dice_tables, bar_collections,
                         self._generate_jinja2_environment(data_name), midi_settings)
