__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"



class Measure(object):

    def __init__(self, bars, alternatives=None):
        """Information about a single measure for all instruments/hands.

        Args:
            bars (list of Bar): the bars in this measure, one per hand / instrument
            alternatives (list of Measure): alternative Measures, if set this means this measure is a repeat measure
                which should be rendered as part 1, repeat, part 2.
        """
        self.bars = bars
        self.alternatives = alternatives


class Bar(object):

    def __init__(self, lilypond_code, alternatives=None):
        """Single bar for a single instrument / hand.

        Args:
            lilypond_code (str): the lilypond code for this single bar
            alternative (list of Bar): list of alternative bars (used for repeats, like in part 1, repeat, part 2).
        """
        self.lilypond_code = lilypond_code
        self.alternatives = alternatives

    def __str__(self):
        return self.lilypond_code


class KeySignature(object):

    def __init__(self, note, is_major):
        """The key signature for a single tract.

        Args:
            note: the base note of this key
            is_major: if this is a major key, if this is false we assume a minor key.
        """
        self.note = note
        self.is_major = is_major

    def __str__(self):
        return self.note + '\\' + 'major' if self.is_major else 'minor'


class TimeSignature(object):

    def __init__(self, nmr_beats, single_beat_value):
        """The time signature for a single tract.

        Args:
            nmr_beats (int): the number of beats in one measure
            single_beat_value (int): the note value which is to be given one beat
        """
        self.nmr_beats = nmr_beats
        self.single_beat_value = single_beat_value

    def __str__(self):
        return str(self.nmr_beats) + '/' + str(self.single_beat_value)
