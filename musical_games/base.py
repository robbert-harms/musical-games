__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


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

    def __init__(self, note, major_minor):
        """The key signature for a single tract.

        Args:
            note (str): the base note of this key
            major_minor (str): either 'major' or 'minor'
        """
        self.note = note
        self.major_minor = major_minor

        if self.major_minor != 'major' and self.major_minor != 'minor':
            raise ValueError('The value for major_minor is not one of \'major\' or \'minor\'. '
                             'Value given: {}'.format(major_minor))

    def __str__(self):
        return self.note + '\\' + self.major_minor


class TimeSignature(object):

    def __init__(self, nmr_beats, beat_value):
        """The time signature for a single tract.

        Args:
            nmr_beats (int): the number of beats in one measure
            beat_value (int): the note value which is to be given one beat
        """
        self.nmr_beats = nmr_beats
        self.beat_value = beat_value

    def __str__(self):
        return str(self.nmr_beats) + '/' + str(self.beat_value)


class TempoIndication(object):

    def __init__(self, beat_value, mm_tempo):
        """The time signature for a single tract.

        Args:
            beat_value (int): the beat that we indicate the tempo for. Example: (2, 4, 8, ...)
            mm_tempo (int): the Malzel Metronome value (for example: 120)
        """
        self.beat_value = beat_value
        self.mm_tempo = mm_tempo

    def __str__(self):
        return str(self.beat_value) + ' = ' + str(self.mm_tempo)