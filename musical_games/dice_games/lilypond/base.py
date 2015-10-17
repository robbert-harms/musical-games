from musical_games.utils import correct_indent

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class LilypondTypesetInterface(object):

    def typeset(self):
        """Create and return a typesetted document string from this typesetter.

        This should return a string containing the entire typesetted lilypond file.

        Returns:
            str: the lilypond typesetted results
        """


class MusicBookTypeset(LilypondTypesetInterface):

    def __init__(self, pieces):
        self._pieces = pieces
        self._lilypond_version = '2.18.2'
        self.comments = []
        self.page_limit = None
        self.ragged_right = None
        self.title = ''

    def add_comments(self, comments):
        if isinstance(comments, MusicBookComment):
            self.comments.append(comments)
        else:
            self.comments.extend(comments)

    def typeset(self):
        parts = []
        parts.append('\\version "{}"'.format(self._lilypond_version))
        parts.append('\include "articulate.ly"')

        parts.append(self._get_paper_settings())
        parts.append(self._get_header())

        for piece in self._pieces:
            parts.append(correct_indent(piece.typeset(), 0))

        parts.append(self._get_comments())
        return "\n".join(parts)

    def _get_comments(self):
        parts = []
        for comment in self.comments:
            # double braces escape the braces when using the format function.
            parts.append('\markup {{\\fill-line \italic {{"{0}" "{1}" "{2}"}}}}'.format(comment.left, comment.middle,
                                                                                        comment.right))
        return "\n".join(parts)

    def _get_header(self):
        title = self.title
        if title is None:
            title = ''

        parts = ['\header{',
                 "\t title = \"{}\" ".format(title),
                 "\t tagline = \"\" ",
                 '}']
        return "\n".join(parts)

    def _get_paper_settings(self):
        parts = ['\paper {']

        if self.page_limit is not None:
            parts.append("\t" + 'page-count = {}'.format(self.page_limit))

        if self.ragged_right is not None:
            parts.append("\t" + 'ragged-right = ##{}'.format('t' if self.ragged_right else 'f'))

        parts.append(correct_indent(r'''
            print-all-headers = ##t
            score-markup-spacing = #'((basic-distance . 10))
            markup-system-spacing #'minimum-distance = 0

            scoreTitleMarkup = \markup {
                \override #'(baseline-skip . 10) %% changes the distance between title/subtitle and composer/arranger
                \column {
                    \override #'(baseline-skip . 3.5)
                    \column {
                        \huge \larger \bold
                        \fill-line {
                            \larger \fromproperty #'header:title
                        }
                        \fill-line {
                            \large \smaller \bold
                            \larger \fromproperty #'header:subtitle
                        }
                        \fill-line {
                            \smaller \bold
                            \fromproperty #'header:subsubtitle
                        }
                    }
                    \override #'(baseline-skip . 3.5)
                    \column {
                        \fill-line {
                            \fromproperty #'header:poet
                            { \large \bold \fromproperty #'header:instrument }
                            \fromproperty #'header:composer
                        }
                        \fill-line {
                            \fromproperty #'header:piece
                            \fromproperty #'header:meter
                            \fromproperty #'header:arranger
                        }
                    }
                }
            }''', 4))
        parts.append('}')
        return "\n".join(parts)


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


class Staff(object):

    def __init__(self, notes, clef):
        """All information needed to render a staff.

        Attributes:
            notes (str): the notes on this staff
            clef (str): the type of clef, lilypond string
            instrument_name (str): the instrument name, if not None we render it next to the staff
        """
        self.notes = notes
        self.clef = clef
        self.instrument_name = ''


class PieceScores(object):

    def typeset(self):
        """Typeset all the information about one piece.

        This typically typesets the score blocks.

        Returns:
            str: the typesetted information about a single piece.
        """

class SimplePieceScore(PieceScores):

    def __init__(self, staffs, unique_id, key_signature, time_signature, tempo, **kwargs):
        """Information of a single piece for use in the MusicBook typesetter.

        Attributes:
            staffs (list of Staff): list of Staffs for each hand/instrument.
            unique_id (str): the unique id for this piece (needed when using multiple pieces).
                This can only contain alpha characters.
            key_signature (KeySignature): the key for this piece
            time_signature (TimeSignature): the time for this piece
            tempo (TempoIndication): the tempo
            display_staff_names (bool): if we want to display the instrument names next to the bars
            display_main_staff_names (bool): if we want to display the single main staff name
            display_all_bar_numbers (bool): if we want to display all bar numbers
            display_tempo_indication (bool): if we want to display the tempo indication
            title (str): the title of this piece
            main_staff_type (str): the lilypond staff group type
            main_staff_name (str): the name of the main lilypond staff
        """
        self.staffs = staffs
        self.unique_id = unique_id
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo = tempo
        self.display_staff_names = False
        self.display_main_staff_name = False
        self.display_all_bar_numbers = False
        self.display_tempo_indication = True
        self.title = ''
        self.main_staff_type = 'PianoStaff'
        self.main_staff_name = 'Piano'

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_from_piece(cls, staffs, piece, **kwargs):
        """Create a piece score using information from a PieceInfo object.

        Args:
            staffs (list of Staff): list of Staffs for each hand/instrument.
            piece (PieceInfo): the piece info we use to fill the basic info
            **kwargs: remaining arguments
        """
        return cls(staffs, piece.name, piece.key_signature, piece.time_signature, piece.tempo, **kwargs)

    def _typeset_staff(self, staff, staff_options=None):
        parts = ['\\new Staff ']

        if staff_options:
            parts.append("\t" + ' \with {')
            parts.append("\t\t" + "\n\t\t".join(staff_options))
            parts.append("\t" + '}')

        parts.append("\t" + '<<')

        parts.append(correct_indent(self._typeset_staff_options(), 4))
        parts.append("\t" + '{')
        parts.append("\t\t" + '\clef {}'.format(staff.clef))

        if self.display_staff_names:
            parts.append("\t\t" + '\set Staff.instrumentName = #"{} "'.format(staff.instrument_name))

        parts.append(correct_indent(staff.notes, 8))

        parts.append("\t" + '}')
        parts.append('>>')
        return "\n".join(parts)

    def _typeset_staff_options(self):
        barnumbers = ''
        if self.display_all_bar_numbers:
            barnumbers = '\\override Score.BarNumber.break-visibility = ##(#t #t #t)'

        tempo = ''
        if self.display_tempo_indication:
            tempo = '\\tempo ' + str(self.tempo)

        return r'''
        {{
            {barnumbers}
            \key {key}
            \time {time}
            {tempo}
            \override Score.RehearsalMark.direction = #down
        }}'''.format(barnumbers=barnumbers, key=self.key_signature,
                     time=self.time_signature, tempo=tempo)


class VisualScore(SimplePieceScore):

    def typeset(self):
        parts = ['\score {',
                 "\t \header {",
                 "\t\t piece = \markup {{ \\fontsize #1 \"{}\"}}".format(self.title if self.title is not None else ' '),
                 "\t\t title = \"\" ",
                 "\t }",
                 "\t \\new {}".format(self.main_staff_type)]

        if self.display_staff_names and self.display_main_staff_name:
            parts.append("\t\t" + ' \with {{instrumentName = {} }}'.format(self.main_staff_name))
        parts.append("\t\t" + '<<')

        for staff in self.staffs:
            parts.append(correct_indent(self._typeset_staff(staff), 4))

        parts.append("\t" + '>>')

        if not self.display_staff_names:
            parts.extend(["\t" + '\layout {',
                          "\t\t" + 'indent = 0\mm',
                          "\t" + '}'])

        parts.append('}')
        return "\n".join(parts)


class MidiScore(SimplePieceScore):

    def __init__(self, *args, **kwargs):
        """The score for the midi output.

        Attributes:
            midi_instruments (list of str): per staff a midi instrument name
            midi_min_volumes (list of float): per staff a minimum volume indication between 0 and 1
            midi_max_volumes (list of float): per staff a maximum volume indication between 0 and 1
        """
        self.midi_instruments = None
        self.midi_min_volumes = None
        self.midi_max_volumes = None
        super(MidiScore, self).__init__(*args, **kwargs)

    def typeset(self):
        parts = ['\score {',
                 "\t \\unfoldRepeats",
                 "\t \\articulate",
                 "\t \\new {} <<".format(self.main_staff_type)]

        for ind, staff in enumerate(self.staffs):
            midi_instrument = self.midi_instruments[ind] if self.midi_instruments else 'acoustic grand'
            midi_min_volume = self.midi_min_volumes[ind] if self.midi_min_volumes else '0.0'
            midi_max_volume = self.midi_max_volumes[ind] if self.midi_max_volumes else '1'

            staff_options = ['midiMinimumVolume = #{}'.format(midi_min_volume),
                             'midiMaximumVolume = #{}'.format(midi_max_volume),
                             'midiInstrument = #"{}" '.format(midi_instrument)]

            parts.append(correct_indent(self._typeset_staff(staff, staff_options), 4))

        parts.append("\t" + '>>')
        parts.append(r'\midi { }')
        parts.append('}')
        return "\n".join(parts)

