from musical_games.dice_games.lilypond.base import TypesetStaffInfo
from musical_games.dice_games.lilypond.staff_builders import AllBarsConcatenated, WithRepeat, NoneAnnotator, \
    FineAtEnd, DaCapoAtEnd
from musical_games.dice_games.lilypond.typesetters import VisualScoreTypeset, MidiScoreTypeset

__author__ = 'Robbert Harms'
__date__ = "2015-12-20"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class CompositionManager(object):
    """Composition managers take care of the order of the scores in the final composition."""

    def get_scores(self, parts, table_indices):
        """Get the scores for all the parts.

        Args:
            parts (list of CompositionPart): the list of parts we want to get the scores from
            table_indices (dict): per musical part and per dice table the list of indices we want to use for that part.
        """


class SimpleCompositionManager(CompositionManager):
    """This composition manager uses the SimpleCompositionPartManager for every composition part."""

    def get_scores(self, parts, table_indices):
        part_manager = SimpleCompositionPartManager()

        scores = []
        for part in parts:
            scores.extend(part.get_composition_scores(table_indices[part.name], part_manager))

        return scores


class SimpleTwoPiece(CompositionManager):
    """This composition manager is meant for compositions consisting of two pieces.

    At the end of the first piece we will add a 'Fine' and at the end of the second piece we will add a 'DC al Fine'.
    Next to that, we will add one extra midi score for the first part without repeats.
    """

    def get_scores(self, parts, table_indices):
        part_managers = [WithFine(), WithDCAlFine()]

        scores = []
        for ind, part in enumerate(parts):
            scores.extend(part.get_composition_scores(table_indices[part.name], part_managers[ind]))

        scores.extend(parts[0].get_composition_scores(table_indices[parts[0].name], OnlyMidi()))

        return scores


class CompositionPartManager(object):
    """Composition managers take care of generating the right scores for a composition.

    You can use this for composition parts that requires a specific staff annotator or generate multiple
    midi scores.
    """

    def get_scores(self, instrument_info, title, bars):
        """Get the scores rendered by this composition part manager.

        Args:
            instrument_info (Instrument): the instrumental information
            title (str): the title of this part
            bars (list of list of Bars): the list of Bars we use per staff

        Returns:
            list of LilypondScore: the list of scores, returned by this manager. Can contain one or more visual and/or
                midi scores.
        """


class SimpleCompositionPartManager(CompositionPartManager):
    """This composition part manager will render one visual and one midi score with repeats."""

    def get_scores(self, instrument_info, title, bars):
        music_expressions = WithRepeat(bars, instrument_info.repeats, self._get_staff_annotator()).typeset()

        staffs = []
        for ind, staff in enumerate(instrument_info.staffs):
            staffs.append(TypesetStaffInfo(
                music_expressions[ind],
                staff.clef,
                staff.key_signature,
                staff.time_signature,
                instrument_name=staff.instrument_name,
                midi_options=staff.midi_options))

        score = VisualScoreTypeset(
            title,
            staffs,
            instrument_info.tempo_indication,
            staff_layout=instrument_info.staff_layout,
            show_tempo_indication=True,
            show_title=True,
            show_bar_numbers=False
        ).typeset()

        midi_score = MidiScoreTypeset(
            title,
            staffs,
            instrument_info.tempo_indication,
        ).typeset()

        return [score, midi_score]

    def _get_staff_annotator(self):
        return NoneAnnotator()


class WithFine(SimpleCompositionPartManager):
    """This composition manager will render one visual and one midi score with at the end a 'Fine'."""

    def _get_staff_annotator(self):
        return FineAtEnd()


class WithDCAlFine(SimpleCompositionPartManager):
    """This composition manager will render one visual and one midi score with at the end a 'D.C al Fine'."""

    def _get_staff_annotator(self):
        return DaCapoAtEnd()


class OnlyMidi(CompositionPartManager):
    """This composition manager only renders a midi score"""

    def get_scores(self, instrument_info, title, bars):
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
        ).typeset()

        return [midi_score]
