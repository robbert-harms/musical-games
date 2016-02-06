from musical_games.dice_games.lilypond.base import TypesetStaffInfo
from musical_games.dice_games.lilypond.staff_builders import AllBarsConcatenated, WithRepeat, NoneAnnotator, \
    FineAtEnd, DaCapoAtEnd, KirnbergerPolonaiseStaffTypesetMidi, \
    KirnbergerPolonaiseStaffTypesetVisual
from musical_games.dice_games.lilypond.typesetters import VisualScoreTypeset, MidiScoreTypeset

__author__ = 'Robbert Harms'
__date__ = "2015-12-20"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class CompositionManager(object):
    """Composition managers take care of the order of the scores in the final composition."""

    def get_scores(self, parts, table_indices, midi_options=None):
        """Get the scores for all the parts.

        Args:
            parts (list of CompositionPart): the list of parts we want to get the scores from
            table_indices (dict): per musical part and per dice table the list of indices we want to use for that part.
            midi_options (dict with list of MidiOption objects): a dictionary with for every part in the
                composition a list with per tract additional midi options. The default is used for options set to None.
        """


class SimpleCompositionManager(CompositionManager):
    """This composition manager uses the SimpleCompositionPartManager for every composition part."""

    def get_scores(self, parts, table_indices, midi_options=None):
        part_manager = SimpleCompositionPartManager(NoneAnnotator())

        scores = []
        for part in parts:
            part_midi_options = midi_options[part.name] if part.name in midi_options else None
            scores.extend(part.get_composition_scores(table_indices[part.name], part_manager,
                                                      midi_options=part_midi_options))

        return scores


class KirnbergerPolonaiseCompositionManager(CompositionManager):
    """This composition manager uses the KirnbergerPolonaisePartManager for rendering the composition."""

    def get_scores(self, parts, table_indices, midi_options=None):
        part_manager = KirnbergerPolonaisePartManager(NoneAnnotator())

        scores = []
        for part in parts:
            part_midi_options = midi_options[part.name] if part.name in midi_options else None
            scores.extend(part.get_composition_scores(table_indices[part.name], part_manager,
                                                      midi_options=part_midi_options))

        return scores


class SimpleTwoPiece(CompositionManager):
    """This composition manager is meant for compositions consisting of two pieces.

    At the end of the first piece we will add a 'Fine' and at the end of the second piece we will add a 'DC al Fine'.
    Next to that, we will add one extra midi score for the first part without repeats.
    """

    def get_scores(self, parts, table_indices, midi_options=None):
        part_managers = [SimpleCompositionPartManager(FineAtEnd()),
                         SimpleCompositionPartManager(DaCapoAtEnd())]

        scores = []
        for ind, part in enumerate(parts):
            part_midi_options = midi_options[part.name] if part.name in midi_options else None
            scores.extend(part.get_composition_scores(table_indices[part.name], part_managers[ind],
                                                      midi_options=part_midi_options))

        part_midi_options = midi_options[parts[0].name] if parts[0].name in midi_options else None
        scores.extend(parts[0].get_composition_scores(table_indices[parts[0].name], MidiAlFine(),
                                                      midi_options=part_midi_options))

        return scores


class CompositionPartManager(object):
    """Composition managers take care of generating the right scores for a composition.

    You can use this for composition parts that requires a specific staff annotator or generate multiple
    midi scores.
    """

    def get_scores(self, instrument_info, title, bars, midi_options=None, show_title=True):
        """Get the scores rendered by this composition part manager.

        Args:
            instrument_info (Instrument): the instrumental information
            title (str): the title of this part
            bars (list of list of Bars): the list of Bars we use per staff
            midi_options (list): if set, a list with extra midi options per tract
            show_title (bool): if we show the title of this part in visual scores

        Returns:
            list of LilypondScore: the list of scores, returned by this manager. Can contain one or more visual and/or
                midi scores.
        """


class SimpleCompositionPartManager(CompositionPartManager):
    """This composition part manager will render one visual and one midi score with repeats."""

    def __init__(self, staff_annotator):
        super(SimpleCompositionPartManager, self).__init__()
        self._staff_annotator = staff_annotator

    def get_scores(self, instrument_info, title, bars, midi_options=None, show_title=True):
        return [self._get_visual_score(
                    instrument_info, title, bars,
                    WithRepeat(bars, instrument_info.repeats, self._staff_annotator), show_title),
                self._get_midi_score(
                    instrument_info, title, bars,
                    WithRepeat(bars, instrument_info.repeats, self._staff_annotator), midi_options)]

    def _get_visual_score(self,  instrument_info, title, bars, staff_builder, show_title):
        music_expressions = staff_builder.typeset()

        staffs = []
        for ind, staff in enumerate(instrument_info.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        return VisualScoreTypeset(
            title,
            staffs,
            instrument_info.tempo_indication,
            staff_layout=instrument_info.staff_layout,
            show_tempo_indication=True,
            show_title=show_title,
            show_bar_numbers=False
        ).typeset()

    def _get_midi_score(self, instrument_info, title, bars, staff_builder, midi_options):
        music_expressions = staff_builder.typeset()

        staffs = []
        for ind, staff in enumerate(instrument_info.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        return MidiScoreTypeset(
            title,
            staffs,
            instrument_info.tempo_indication,
            midi_options=midi_options
        ).typeset()


class KirnbergerPolonaisePartManager(SimpleCompositionPartManager):
    """This composition part manager will render one visual and one midi score with repeats."""

    def get_scores(self, instrument_info, title, bars, midi_options=None, show_title=True):
        return [self._get_visual_score(instrument_info, title, bars,
                                       KirnbergerPolonaiseStaffTypesetVisual(bars), show_title),
                self._get_midi_score(instrument_info, title, bars,
                                     KirnbergerPolonaiseStaffTypesetMidi(bars), midi_options)]


class MidiAlFine(CompositionPartManager):
    """This composition manager only renders a midi score"""

    def get_scores(self, instrument_info, title, bars, midi_options=None, show_title=True):
        music_expressions = AllBarsConcatenated(bars, instrument_info.bar_converter).typeset()

        staffs = []
        for ind, staff in enumerate(instrument_info.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        midi_score = MidiScoreTypeset(
            title + ' Al Fine',
            staffs,
            instrument_info.tempo_indication,
            midi_options=midi_options
        ).typeset()

        return [midi_score]
