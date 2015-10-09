from pkg_resources import resource_filename

from musical_games.base import KeySignature, TimeSignature, TempoIndication
from musical_games.dice_games.base import PieceInfo, TractInfo, DiceTable
from musical_games.dice_games.lilypond.typeset_staff import NoRepeat, MozartNoRepeat
from musical_games.dice_games.utils import load_bars_from_file, load_dice_table
from musical_games.dice_games.lilypond.base import MusicBookTypeset, PieceScores, MusicBookComment, VisualScore, Staff

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
    def id(self):
        """Get an ID of this work. This should only contain alphanumeric chars and underscore.

        Returns:
            str: the ID key of this work.
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

    def __init__(self, name, id, instrumental_settings, composition_base_class):
        self._name = name
        self._id = id
        self._instrumental_settings = instrumental_settings
        self._composition_base_class = composition_base_class

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def get_available_instrumental_settings(self):
        return self._instrumental_settings

    def get_composition(self, instrumental_setting):
        return self._composition_base_class(instrumental_setting)


class KirnbergerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerMenuetTrioInfo, self).__init__(
            'Menuet / Trio', 'menuet_trio',
            KirnbergerMenuetTrio.supported_instrumental_settings,
            KirnbergerMenuetTrio)


class KirnbergerPolonaiseInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerPolonaiseInfo, self).__init__('Polonaise', 'polonaise',
                                                      ['piano', 'chamber_ensemble'], KirnbergerPolonaise)


class StadlerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(StadlerMenuetTrioInfo, self).__init__('Menuet / Trio', 'menuet_trio', ['piano'], StadlerMenuetTrio)


class MozartWaltzInfo(BasicCompositionInfo):

    def __init__(self):
        super(MozartWaltzInfo, self).__init__(
            'Waltz', 'waltz',
            MozartWaltz.supported_instrumental_settings,
            MozartWaltz)


class Composition(object):

    def __init__(self, instrumental_setting):
        self.instrumental_setting = instrumental_setting


class KirnbergerMenuetTrio(Composition):

    supported_instrumental_settings = ['piano', 'chamber_ensemble']

    def __init__(self, instrumental_setting):
        super(KirnbergerMenuetTrio, self).__init__(instrumental_setting)

        self._dice_tables = [
            DiceTable('Kirnberger Menuet',
                      load_dice_table(resource_filename('musical_games',
                                                        'data/kirnberger/menuet_trio/table_menuet.txt'))),
            DiceTable('Kirnberger Trio',
                      load_dice_table(resource_filename('musical_games',
                                                        'data/kirnberger/menuet_trio/table_trio.txt'))),
        ]

        self._pieces = [
            PieceInfo(
                'Menuet',
                [TractInfo('Left hand', 'treble', load_bars_from_file(
                    resource_filename(
                        'musical_games',
                        'data/kirnberger/menuet_trio/{}/bars_menuet_lh.txt'.format(self.instrumental_setting)))),
                 TractInfo('Right hand', 'bass', load_bars_from_file(
                     resource_filename(
                         'musical_games',
                         'data/kirnberger/menuet_trio/{}/bars_menuet_rh.txt'.format(self.instrumental_setting))))],
                KeySignature('d', 'major'),
                TimeSignature(3, 4),
                TempoIndication(4, 100)
            ),
            PieceInfo(
                'Trio',
                [TractInfo('Left hand', 'treble', load_bars_from_file(
                    resource_filename(
                        'musical_games',
                        'data/kirnberger/menuet_trio/{}/bars_trio_lh.txt'.format(self.instrumental_setting)))),
                 TractInfo('Right hand', 'bass', load_bars_from_file(
                     resource_filename(
                         'musical_games',
                         'data/kirnberger/menuet_trio/{}/bars_trio_rh.txt'.format(self.instrumental_setting))))],
                KeySignature('f', 'major'),
                TimeSignature(3, 4),
                TempoIndication(4, 80)
            )
        ]

    def typeset_measure_overview(self):
        # staffs = NoRepeat(self._pieces[0].tract_info).get_staffs()
        #
        # waltz_visual = VisualScore(
        #     staffs,
        #     'waltz',
        #     self._pieces[0].key_signature,
        #     self._pieces[0].time_signature,
        #     self._pieces[0].tempo)
        #
        # waltz_visual.display_all_bar_numbers = True
        # waltz_visual.display_tempo_indication = False
        # waltz_visual.title = None
        #
        # typesetter = MusicBookTypeset([waltz_visual])
        # typesetter.title = 'Mozart Measures'
        # return typesetter.typeset()
        #todo
        pass


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
    def id(self):
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
    def id(self):
        return 'menuet_trio'

    def get_instrument_setting_names(self):
        return [PianoSolo([PieceInfo(), PieceInfo()])]


class MozartWaltz(Composition):

    supported_instrumental_settings = ('piano',)

    def __init__(self, instrumental_setting):
        super(MozartWaltz, self).__init__(instrumental_setting)

        self._dice_tables = [
            DiceTable('Mozart Waltz',
                      load_dice_table(resource_filename('musical_games', 'data/mozart/waltz/table.txt')))
        ]

        self._pieces = [
            PieceInfo(
                'Waltz',
                [TractInfo('Left hand', 'treble', load_bars_from_file(
                    resource_filename('musical_games', 'data/mozart/waltz/piano/bars_lh.txt'))),
                 TractInfo('Right hand', 'bass', load_bars_from_file(
                     resource_filename('musical_games', 'data/mozart/waltz/piano/bars_rh.txt')))],
                KeySignature('c', 'major'),
                TimeSignature(3, 8),
                TempoIndication(8, 110)
            )
        ]

    def typeset_measure_overview(self):
        staffs = MozartNoRepeat(self._pieces[0].tract_info).get_staffs()

        waltz_visual = VisualScore(
            staffs,
            'waltz',
            self._pieces[0].key_signature,
            self._pieces[0].time_signature,
            self._pieces[0].tempo)

        waltz_visual.display_all_bar_numbers = True
        waltz_visual.display_tempo_indication = False
        waltz_visual.title = None

        typesetter = MusicBookTypeset([waltz_visual])
        typesetter.title = 'Mozart Measures'
        return typesetter.typeset()