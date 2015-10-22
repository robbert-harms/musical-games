from collections import OrderedDict
from pkg_resources import resource_filename
import six

from musical_games.base import KeySignature, TimeSignature, TempoIndication
from musical_games.dice_games.base import PieceInfo, TractInfo, DiceTable
from musical_games.dice_games.lilypond.staff_builders import AllBarsConcatenated, MozartAllBarsConcatenated, \
    MozartSingleMeasure, SingleMeasure, NoRepeat, WithRepeat
from musical_games.dice_games.lilypond.staff_annotators import FineAtEnd, DaCapoAtEnd
from musical_games.dice_games.utils import load_bars_from_file, load_dice_table, find_double_bars
from musical_games.dice_games.lilypond.base import MusicBookTypeset, PieceScores, MusicBookComment, VisualScore, \
    Staff, MidiScore

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
        """Abstract implementation class of CompositionInfo"""
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
        """Load a composition for the given instrumental setting.

        Args:
            instrumental_setting (str of InstrumentalSetting): if it is a string we try to match it to the known
                instrumental settings in this composition info class.

        Returns:
            Composition: the composition object, loaded for the given instrumental setting
        """
        if isinstance(instrumental_setting, six.string_types):
            ins_setting = None
            for ins_set in self._instrumental_settings:
                if ins_set.id == instrumental_setting:
                    ins_setting = ins_set
                    break
            if not ins_setting:
                raise ValueError('The instrumental setting with the '
                                 'id {} could not be found.'.format(instrumental_setting))
            instrumental_setting = ins_setting

        return self._composition_base_class(instrumental_setting)


class InstrumentalSetting(object):

    def __init__(self, name, id):
        """Structure for holding information about a instrumental setting."""
        self.name = name
        self.id = id


class KirnbergerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerMenuetTrioInfo, self).__init__(
            'Menuet / Trio',
            'menuet_trio',
            KirnbergerMenuetTrio.supported_instrumental_settings,
            KirnbergerMenuetTrio)


class KirnbergerPolonaiseInfo(BasicCompositionInfo):

    def __init__(self):
        super(KirnbergerPolonaiseInfo, self).__init__(
            'Polonaise',
            'polonaise',
            KirnbergerPolonaise.supported_instrumental_settings,
            KirnbergerPolonaise)


class StadlerMenuetTrioInfo(BasicCompositionInfo):

    def __init__(self):
        super(StadlerMenuetTrioInfo, self).__init__(
            'Menuet / Trio',
            'menuet_trio',
            StadlerMenuetTrio.supported_instrumental_settings,
            StadlerMenuetTrio)


class MozartWaltzInfo(BasicCompositionInfo):

    def __init__(self):
        super(MozartWaltzInfo, self).__init__(
            'Waltz', 'waltz',
            MozartWaltz.supported_instrumental_settings,
            MozartWaltz)


class Composition(object):

    def __init__(self, instrumental_setting):
        """Holds basic information about a composition and is able to create various views on the composition."""
        self.instrumental_setting = instrumental_setting
        self._dice_tables = []
        self._pieces = OrderedDict()

    def get_pieces_names(self):
        """Get the names of the individual pieces in this composition.

        Returns:
            list of str: list of piece names
        """
        return self._pieces.keys()

    def get_dice_tables(self):
        """Get the dice tables used by this composition.

        Returns:
            list of DiceTable: list of all the available dice tables.
        """
        return self._dice_tables

    def count_unique_compositions(self):
        """Get a count of the number of unique compositions possible from this composition.

        Returns:
            int: the number of unique compositions
        """

    def get_similar_measures_list(self, dice_table):
        """Get a list of the double/similar measures for this dice table.

        Args:
            dice_table (DiceTable): the dice table for which we want the list of similar measures

        Returns:
            list of list: the list of similar measures
        """

    def typeset_measure_overview(self, piece_name=None):
        """Typeset the overview of the measures.

        Args:
            piece_name (str): the name of a piece we want to get the measures overview of. If not given,
                a single lilypond string with all the pieces should be returned.

        Returns:
            str: lilypond code for the measures overview
        """

    def typeset_composition(self, table_indices, comments=()):
        """Typeset a whole composition with all the pieces.

        Args:
            table_indices (dict): as keys the names of the dice tables, as values the list of indices we wish to
                use for the composition
            comments (list of MusicBookComment): the list of comments we append at the end of the compositions

        Returns:
            str: lilypond code for a composition
        """

    def typeset_single_measure(self, dice_table_name, measure_index):
        """Typeset a single measure.

        This is supposed to be used to illustrate a single measure referenced in one of the dice tables.

        The default implementation assumes that there is a one-on-one match between the dice tables and the pieces and
        that the pieces and the dice tables are named similar.

        Args:
            dice_table_name (str): the name of the dice table we reference
            measure_index (int): the index (1 based) from the table.

        Returns:
            str: lilypond code for viewing just that single measure.
        """
        piece = self._pieces[dice_table_name]
        score = VisualScore.create_from_piece(
            SingleMeasure(piece.tract_info, measure_index).get_staffs(),
            piece,
            display_all_bar_numbers=False,
            display_tempo_indication=False,
            title=None
        )
        typesetter = MusicBookTypeset([score])
        typesetter.title = None
        return typesetter.typeset()

    def get_composition_audio_names(self):
        """Get the audio names for the midi sections in the composition typesets.

        Returns:
            list of str: the pretty print names of the audio files in the composition
        """

    def _get_measure_overview_scores(self, piece_name=None):
        """Get the scores for an overview of the measures.

        This is a helper method to save space in the implementations.

        Returns:
            scores: score objects to be used in a typesetter.
        """
        scores = []
        for piece in self._pieces.values():
            if piece_name is None or piece_name == piece.name:
                score = VisualScore.create_from_piece(
                    AllBarsConcatenated(piece.tract_info).get_staffs(),
                    piece,
                    display_all_bar_numbers=True,
                    display_tempo_indication=False,
                    title=piece.name
                )
                scores.append(score)
        return scores

    def _get_basic_composition_scores(self, table_indices):
        """Get the scores for a basic composition.

        This is a helper method to save space in the implementations. This function has a few assumptions
        about the information in the pieces. See the code for details.

        Returns:
            scores: score objects to be used in a typesetter.
        """
        scores = []
        for dice_table_name, indices in table_indices.items():
            piece = self._pieces[dice_table_name]
            staffs = WithRepeat(piece.tract_info, indices, piece.repeat_moments).get_staffs()

            visual = VisualScore.create_from_piece(staffs, piece, display_all_bar_numbers=False,
                                                   display_tempo_indication=True, title=piece.name)
            scores.append(visual)

            midi = MidiScore.create_from_piece(staffs, piece, midi_max_volumes=piece.midi_max_volumes)
            scores.append(midi)
        return scores

    def _get_menuet_trio_scores(self, table_indices):
        """Get the scores for a basic composition.

        This is a helper method to save space in the implementations. This function has a few assumptions
        about the information in the pieces. See the code for details.

        This function adds da capo al fine messages between the menuet and trio, and adds the audio for the
        menuet again, without the repetitions.

        Returns:
            scores: score objects to be used in a typesetter.
        """
        scores = []
        for dice_table_name, indices in table_indices.items():
            if dice_table_name == 'Menuet':
                staff_annotator = FineAtEnd()
            else:
                staff_annotator = DaCapoAtEnd()

            piece = self._pieces[dice_table_name]
            staffs = WithRepeat(piece.tract_info, indices, piece.repeat_moments,
                                staff_annotator=staff_annotator).get_staffs()

            visual = VisualScore.create_from_piece(staffs, piece, display_all_bar_numbers=False,
                                                   display_tempo_indication=True, title=piece.name)
            scores.append(visual)

            midi = MidiScore.create_from_piece(staffs, piece, midi_max_volumes=piece.midi_max_volumes)
            scores.append(midi)

        piece = self._pieces['Menuet']
        indices = table_indices['Menuet']
        staffs = NoRepeat(piece.tract_info, indices, piece.repeat_moments).get_staffs()
        midi_no_repeat = MidiScore.create_from_piece(staffs, piece, midi_max_volumes=piece.midi_max_volumes)
        scores.append(midi_no_repeat)

        return scores

    def _load_bars(self, bar_file):
        return load_bars_from_file(resource_filename('musical_games', bar_file))


class KirnbergerMenuetTrio(Composition):

    supported_instrumental_settings = (InstrumentalSetting('Piano', 'piano'),
                                       InstrumentalSetting('Chamber ensemble', 'chamber_ensemble'))

    def __init__(self, instrumental_setting):
        super(KirnbergerMenuetTrio, self).__init__(instrumental_setting)

        self._dice_tables = [
            DiceTable(
                'Menuet',
                load_dice_table(resource_filename('musical_games', 'data/kirnberger/menuet_trio/table_menuet.txt'))),
            DiceTable(
                'Trio',
                load_dice_table(resource_filename('musical_games', 'data/kirnberger/menuet_trio/table_trio.txt'))),
        ]

        if self.instrumental_setting.id == 'piano':
            bar_dicts_menuet = list(map(self._load_bars, [
                'data/kirnberger/menuet_trio/piano/bars_menuet_lh.txt',
                'data/kirnberger/menuet_trio/piano/bars_menuet_rh.txt'
            ]))

            bar_dicts_trio = list(map(self._load_bars, [
                'data/kirnberger/menuet_trio/piano/bars_trio_lh.txt',
                'data/kirnberger/menuet_trio/piano/bars_trio_rh.txt'
            ]))

            self._doubles_list_menuet = find_double_bars(bar_dicts_menuet)
            self._doubles_list_trio = find_double_bars(bar_dicts_trio)

            self._pieces = OrderedDict([
                ('Menuet', PieceInfo(
                    'Menuet',
                    [TractInfo('Left hand', 'treble', bar_dicts_menuet[0]),
                     TractInfo('Right hand', 'bass', bar_dicts_menuet[1])],
                    KeySignature('d', 'major'),
                    TimeSignature(3, 4),
                    TempoIndication(4, 100),
                    repeat_moments=[8, 16],
                    midi_max_volumes=[1, 0.75],
                )),
                ('Trio', PieceInfo(
                    'Trio',
                    [TractInfo('Left hand', 'treble', bar_dicts_trio[0]),
                     TractInfo('Right hand', 'bass', bar_dicts_trio[1])],
                    KeySignature('f', 'major'),
                    TimeSignature(3, 4),
                    TempoIndication(4, 80),
                    repeat_moments=[8, 16],
                    midi_max_volumes=[1, 0.75],
                ))
            ])

    def typeset_measure_overview(self, piece_name=None):
        scores = self._get_measure_overview_scores()
        typesetter = MusicBookTypeset(scores)
        typesetter.title = 'Kirnberger Measures'

        if piece_name is not None:
            typesetter.page_limit = 2
        else:
            typesetter.page_limit = 4

        return typesetter.typeset()

    def typeset_composition(self, table_indices, comments=()):
        scores = self._get_menuet_trio_scores(table_indices)
        typesetter = MusicBookTypeset(scores)
        typesetter.add_comments(comments)
        typesetter.title = None
        return typesetter.typeset()

    def count_unique_compositions(self):
        return (self._dice_tables[0].count_unique_combinations(self._doubles_list_menuet)
                * self._dice_tables[1].count_unique_combinations(self._doubles_list_trio))

    def get_similar_measures_list(self, dice_table):
        if dice_table.name == 'Menuet':
            return self._doubles_list_menuet
        else:
            return self._doubles_list_trio

    def get_composition_audio_names(self):
        return ['Menuet', 'Trio', 'Menuet al Fine']


class KirnbergerPolonaise(KirnbergerMenuetTrio):# todo change base class to composition and implement

    supported_instrumental_settings = (InstrumentalSetting('Chamber ensemble', 'chamber_ensemble'),)




class StadlerMenuetTrio(Composition):

    supported_instrumental_settings = (InstrumentalSetting('Piano', 'piano'),)

    def __init__(self, instrumental_setting):
        super(StadlerMenuetTrio, self).__init__(instrumental_setting)

        self._dice_tables = [
            DiceTable('Menuet',
                      load_dice_table(resource_filename('musical_games', 'data/stadler/menuet_trio/table_menuet.txt'))),
            DiceTable('Trio',
                      load_dice_table(resource_filename('musical_games', 'data/stadler/menuet_trio/table_trio.txt')))
        ]

        if self.instrumental_setting.id == 'piano':
            bar_dicts_menuet = list(map(self._load_bars, [
                'data/stadler/menuet_trio/piano/bars_menuet_lh.txt',
                'data/stadler/menuet_trio/piano/bars_menuet_rh.txt'
            ]))

            bar_dicts_trio = list(map(self._load_bars, [
                'data/stadler/menuet_trio/piano/bars_trio_lh.txt',
                'data/stadler/menuet_trio/piano/bars_trio_rh.txt'
            ]))

            self._doubles_list_menuet = find_double_bars(bar_dicts_menuet)
            self._doubles_list_trio = find_double_bars(bar_dicts_trio)

            self._pieces = OrderedDict([
                ('Menuet', PieceInfo(
                    'Menuet',
                    [TractInfo('Left hand', 'treble', bar_dicts_menuet[0]),
                     TractInfo('Right hand', 'bass', bar_dicts_menuet[1])],
                    KeySignature('d', 'major'),
                    TimeSignature(3, 4),
                    TempoIndication(4, 100),
                    repeat_moments=[8, 16],
                    midi_max_volumes=[1, 0.75],
                )),
                ('Trio', PieceInfo(
                    'Trio',
                    [TractInfo('Left hand', 'treble', bar_dicts_trio[0]),
                     TractInfo('Right hand', 'bass', bar_dicts_trio[1])],
                    KeySignature('g', 'major'),
                    TimeSignature(3, 4),
                    TempoIndication(4, 80),
                    repeat_moments=[8, 16],
                    midi_max_volumes=[1, 0.75],
                ))
            ])

    def typeset_measure_overview(self, piece_name=None):
        scores = self._get_measure_overview_scores()
        typesetter = MusicBookTypeset(scores)
        typesetter.title = 'Stadler Measures'
        return typesetter.typeset()

    def typeset_composition(self, table_indices, comments=()):
        scores = self._get_menuet_trio_scores(table_indices)
        typesetter = MusicBookTypeset(scores)
        typesetter.add_comments(comments)
        typesetter.title = None
        typesetter.page_limit = 1
        return typesetter.typeset()

    def count_unique_compositions(self):
        return (self._dice_tables[0].count_unique_combinations(self._doubles_list_menuet)
                * self._dice_tables[1].count_unique_combinations(self._doubles_list_trio))

    def get_similar_measures_list(self, dice_table):
        if dice_table.name == 'Menuet':
            return self._doubles_list_menuet
        else:
            return self._doubles_list_trio

    def get_composition_audio_names(self):
        return ['Menuet', 'Trio', 'Menuet al Fine']

class MozartWaltz(Composition):

    supported_instrumental_settings = (InstrumentalSetting('Piano', 'piano'),)

    def __init__(self, instrumental_setting):
        super(MozartWaltz, self).__init__(instrumental_setting)

        self._waltz_name = 'Waltz'

        self._dice_tables = [
            DiceTable(self._waltz_name,
                      load_dice_table(resource_filename('musical_games', 'data/mozart/waltz/table.txt')))
        ]

        bar_dicts = list(map(self._load_bars, ['data/mozart/waltz/piano/bars_lh.txt',
                                               'data/mozart/waltz/piano/bars_rh.txt']))

        self._doubles_list = find_double_bars(bar_dicts)

        self._pieces = OrderedDict([
            (self._waltz_name, PieceInfo(
                self._waltz_name,
                [TractInfo('Left hand', 'treble', bar_dicts[0]),
                 TractInfo('Right hand', 'bass', bar_dicts[1])],
                KeySignature('c', 'major'),
                TimeSignature(3, 8),
                TempoIndication(8, 110),
                repeat_moments=[8, 16],
                midi_max_volumes=[1, 0.75],
            ))
        ])

    def typeset_single_measure(self, dice_table_name, measure_index):
        piece = self._pieces[dice_table_name]
        waltz_visual = VisualScore.create_from_piece(
            MozartSingleMeasure(piece.tract_info, measure_index).get_staffs(),
            piece,
            display_all_bar_numbers=False,
            display_tempo_indication=False,
            title=None
        )
        typesetter = MusicBookTypeset([waltz_visual])
        typesetter.title = None
        return typesetter.typeset()

    def typeset_measure_overview(self, piece_name=None):
        piece = self._pieces[self._waltz_name]
        waltz_visual = VisualScore.create_from_piece(
            MozartAllBarsConcatenated(piece.tract_info).get_staffs(),
            piece,
            display_all_bar_numbers=True,
            display_tempo_indication=False,
            title=None
        )
        typesetter = MusicBookTypeset([waltz_visual])
        typesetter.title = 'Mozart Measures'
        return typesetter.typeset()

    def typeset_composition(self, table_indices, comments=()):
        scores = self._get_basic_composition_scores(table_indices)
        typesetter = MusicBookTypeset(scores)
        typesetter.add_comments(comments)
        typesetter.title = None
        return typesetter.typeset()

    def count_unique_compositions(self):
        return self._dice_tables[0].count_unique_combinations(self._doubles_list)

    def get_similar_measures_list(self, dice_table):
        return self._doubles_list

    def get_composition_audio_names(self):
        return ['Waltz']