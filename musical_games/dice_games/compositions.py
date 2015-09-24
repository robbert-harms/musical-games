from pkg_resources import resource_filename
from musical_games.base import KeySignature, TimeSignature, TempoIndication
from musical_games.dice_games.base import PieceInfo, BarList, load_bars_from_file, load_dice_table, DiceTable

__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class CompositionInfo(object):

    @property
    def name(self):
        """Returns the name of this work.

        Returns:
            str: the name of this work
        """
        return ''

    @property
    def safe_name(self):
        """Get a safe name of this work. This should only contain alphanumeric signs and underscore.

        Returns:
            str: the safe name of this work.
        """
        return ''

    def get_available_instrumental_settings(self):
        """Get a list of available instrumental settings we can use to generate a composition instance.

        Returns:
            list of str: list of instrumental settings available for this composition.
        """

    def get_composition(self, instrumental_setting):
        """Get an instance of a composition from this composition info.

        Returns:
            Composition: an actual composition object for the given instrumental setting.
        """


class BasicCompositionInfo(CompositionInfo):

    def __init__(self, name, safe_name, instrumental_settings, composition_base_class):
        self._name = name
        self._safe_name = safe_name
        self._instrumental_settings = instrumental_settings
        self._composition_base_class = composition_base_class

    @property
    def name(self):
        return self._name

    @property
    def safe_name(self):
        return self._safe_name

    def get_available_instrumental_settings(self):
        return self._instrumental_settings

    def get_composition(self, instrumental_setting):
        return self._composition_base_class(instrumental_setting)


class Composition(object):

    def __init__(self, instrumental_setting):
        self.instrumental_setting = instrumental_setting


class KirnbergerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerMenuetTrioInfo, self).__init__('Menuet / Trio', 'menuet_trio',
                                                       ['piano', 'chamber_ensemble'], KirnbergerMenuetTrio)


class KirnbergerPolonaiseInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerPolonaiseInfo, self).__init__('Polonaise', 'polonaise',
                                                      ['piano', 'chamber_ensemble'], KirnbergerPolonaise)


class StadlerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(StadlerMenuetTrioInfo, self).__init__('Menuet / Trio', 'menuet_trio', ['piano'], StadlerMenuetTrio)


class MozartWaltzInfo(BasicCompositionInfo):

    def __init__(self):
        super(MozartWaltzInfo, self).__init__('Waltz', 'waltz', ['piano'], MozartWaltz)



class KirnbergerMenuetTrio(Composition):

    def __init__(self):
        super(KirnbergerMenuetTrio, self).__init__()
        self.dice_tables = [
            DiceTable('Kirnberger Menuet',
                      load_dice_table(resource_filename('musical_games',
                                                        'data/kirnberger/menuet_trio/table_menuet.txt'))),
            DiceTable('Kirnberger Trio',
                      load_dice_table(resource_filename('musical_games',
                                                        'data/kirnberger/menuet_trio/table_trio.txt'))),
        ]

    @property
    def name(self):
        return 'Menuet / Trio'

    @property
    def safe_name(self):
        return 'menuet_trio'

    def get_instrument_setting_names(self):
        return [PianoSolo([PieceInfo(''), PieceInfo()]),
                ChamberMusic([PieceInfo(), PieceInfo()])]


class KirnbergerPolonaise(Composition):

    def __init__(self):
        super(KirnbergerPolonaise, self).__init__()
        self.dice_tables = [
            DiceTable('Kirnberger polonaise',
                      load_dice_table(resource_filename('musical_games', 'data/stadler/polonaise/table.txt')))
        ]

    @property
    def name(self):
        return 'Polonaise'

    @property
    def safe_name(self):
        return 'polonaise'

    def get_instrument_setting_names(self):
        return [PianoSolo([PieceInfo('')]),
                ChamberMusic([PieceInfo()])]



class StadlerMenuetTrio(Composition):

    def __init__(self):
        super(StadlerMenuetTrio, self).__init__()
        self.dice_tables = [
            DiceTable('Stadler Menuet',
                      load_dice_table(resource_filename('musical_games', 'data/stadler/menuet_trio/table_menuet.txt'))),
            DiceTable('Stadler Trio',
                      load_dice_table(resource_filename('musical_games', 'data/stadler/menuet_trio/table_trio.txt')))
        ]

    @property
    def name(self):
        return 'Menuet / Trio'

    @property
    def safe_name(self):
        return 'menuet_trio'

    def get_instrument_setting_names(self):
        return [PianoSolo([PieceInfo(), PieceInfo()])]


class MozartWaltz(Composition):

    def __init__(self, instrumental_setting):
        super(MozartWaltz, self).__init__(instrumental_setting)

        self._dice_tables = [
            DiceTable('Mozart Waltz',
                      load_dice_table(resource_filename('musical_games', 'data/mozart/waltz/table.txt')))
        ]

        self._pieces = [
            PieceInfo(
                'Waltz',
                [BarList('Left hand', load_bars_from_file(
                    resource_filename('musical_games', 'data/mozart/waltz/piano/bars_lh.txt'))),
                 BarList('Right hand', load_bars_from_file(
                     resource_filename('musical_games', 'data/mozart/waltz/piano/bars_rh.txt')))],
                KeySignature('c', 'major'),
                TimeSignature(3, 8),
                TempoIndication(8, 110)
            )
        ]

    @property
    def name(self):
        return 'Waltz'

    @property
    def safe_name(self):
        return 'waltz'

    def get_pieces_names(self):
        return [p.name for p in self._pieces]

    def get_music_piece(self, music_piece_name):
        for music_piece in self._pieces:
            if music_piece.name == music_piece_name:
                return music_piece
        raise ValueError('The music piece with the name {} could not be found.'.format(music_piece_name))

    def get_dice_tables(self):
        return self._dice_tables

    def typeset_single_measure(self, music_piece_name, dice_table_name, measure_ind):
        music_piece = self.get_music_piece(music_piece_name)

        # return typesets.SinglePiece()

        pass

    def typeset_measure_overview(self):
        # typeset all the measures how this class likes it best
        # return typesets.MultiPiece()
        pass

    def typeset_composition(self, composition_setting):
        # composition settings contains per dice table a list of requested indices
        # return typesets.MultiPiece()
        pass