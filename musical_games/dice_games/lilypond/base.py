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
        self.force_to_one_page = False
        self.title = ''

    def add_comment(self, comment):
        self.comments.append(comment)

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
        parts = ['\header{',
                 "\t title = \"{}\" ".format(self.title),
                 "\t tagline = \"\" ",
                 '}']
        return "\n".join(parts)

    def _get_paper_settings(self):
        parts = ['\paper {']

        if self.force_to_one_page:
            parts.append("\t" + 'page-count = 1')

        parts.append(correct_indent(r'''
            print-all-headers = ##t
            ragged-right = ##f
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


class VisualScore(PieceScores):

    def __init__(self, staffs, unique_id, key_signature, time_signature, tempo):
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

    def _typeset_staff(self, staff):
        parts = []
        parts.append('\\new Staff <<')
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