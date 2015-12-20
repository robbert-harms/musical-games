__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class TypesetStaffInfo(object):

    def __init__(self, music_expr, clef, key_signature, time_signature, instrument_name, midi_options):
        """All information needed to render a staff.

        Attributes:
            music_expr (str): the actual lilypond code for this staff
            clef (str): the type of clef, lilypond string
            key_signature (KeySignature): the key signature
            time_signature (TimeSignature): the time signature
            instrument_name (str): the instrument name (lilypond instrument type)
            midi_options (MidiOptions): the container for the midi options
        """
        self.music_expr = music_expr
        self.clef = clef
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.instrument_name = instrument_name
        self.midi_options = midi_options


class MusicBookComment(object):

    def __init__(self, left, middle, right):
        """Information about a comment for use in the MusicBookTypesetter.

        Please note that each comment should fit on one line.

        Args:
            left (str): the comment on the left of the page
            middle (str): the comment on the middle of the page
            right (str): the comment on the right of the page
        """
        self.left = left
        self.middle = middle
        self.right = right

    def to_lilypond(self):
        """Return the lilypond version of this comment for at the end of the file.

        Returns:
            str: the lilypond code for this comment
        """
        return '\markup {{\\fill-line \italic {{"{0}" "{1}" "{2}"}}}}'.format(self.left, self.middle, self.right)


class LilypondScore(object):

    def __init__(self, title, score, is_midi_score=False):
        """Container for a single score.

        Args:
            title (str): the title of the score
            score (str): the score itself in string format
            is_midi_score (boolean): if this score is a midi score (if True) or a visual score (if False)

        Attributes:
            title (str): the title of the score
            score (str): the score itself in string format
            is_midi_score (boolean): if this score is a midi score (if True) or a visual score (if False)
        """
        self.title = title
        self.score = score
        self.is_midi_score = is_midi_score


class LilypondBook(object):

    def __init__(self, scores, title, book):
        """Container for a single score.

        Args:
            scores (list of LilypondScore): the list of scores out of which the book was typeset
            title (str): the title of the score
            book (str): the actual typeset book

        Attributes:
            scores (list of LilypondScore): the list of scores out of which the book was typeset
            title (str): the title of the score
            book (str): the actual typeset book
        """
        self.scores = scores
        self.title = title
        self.book = book
