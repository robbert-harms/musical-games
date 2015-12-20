from musical_games.dice_games.lilypond.base import LilypondScore, MusicBookComment, LilypondBook
from musical_games.utils import correct_indent

__author__ = 'Robbert Harms'
__date__ = "2015-12-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class MusicBookTypeset(object):

    def __init__(self, title, scores, show_title=False, comments=None, page_limit=None):
        """Typeset a series of scores into a book.

        Args:
            title (str): the title of the book
            scores (list of LilypondScore): the lilypond scores out of which we create the book
            show_title (bool): if we want to show the titles or not
            comments (list of MusicBookComment): the initial list of music book comments
            page_limit (int): if not None we try to fit all the music on the given number of pages

        """
        self.title = title
        self._scores = scores
        self._lilypond_version = '2.18.2'
        self.comments = comments or []
        self.page_limit = page_limit
        self.ragged_right = None
        self.show_title = show_title

    def add_comments(self, comments):
        """Add one or more comments to this book.

        Args:
            comments (list of MusicBookComment or MusicBookComment): the comments to append after the scores.
        """
        if isinstance(comments, MusicBookComment):
            self.comments.append(comments)
        else:
            self.comments.extend(comments)

    def typeset(self):
        """Typeset the book.

        Returns:
            LilypondBook: the lilypond book
        """
        parts = ['\\version "{}"'.format(self._lilypond_version),
                 '\include "articulate.ly"',
                 self._get_paper_settings(),
                 self._get_header()]

        for score in self._scores:
            parts.append(correct_indent(score.score, 0))

        parts.append("\n".join(comment.to_lilypond() for comment in self.comments))
        return LilypondBook(self._scores, self.title, "\n".join(parts))

    def _get_header(self):
        title = ' '
        if self.show_title:
            title = self.title
        return correct_indent(r'''
            \header{{
                title = "{}"
                tagline = ""
            }}
        '''.format(title), 0)

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


class SimpleScoreTypeset(object):

    def __init__(self, title, staffs, tempo_indication):
        """Information of a single piece for use in the MusicBook typesetter.

        Args:
            title (str): the title for this score
            staffs (list of TypesetStaffInfo): list of Staffs for each instrument.
            tempo_indication (TempoIndication): the tempo indication
        """
        self._title = title
        self.staffs = staffs
        self.tempo_indication = tempo_indication

    def typeset(self):
        """Typeset all the information about one piece.

        This typically typesets the score blocks.

        Returns:
            LilypondScore: the single score in lilypond format
        """


class VisualScoreTypeset(SimpleScoreTypeset):

    def __init__(self, title, staffs, tempo_indication, show_instrument_names=False, show_bar_numbers=False,
                 show_tempo_indication=True, show_title=True):
        """Information of a single piece for use in the MusicBook typesetter.

        Args:
            title (str): the title for this score
            staffs (list of TypesetStaffInfo): list of Staffs for each instrument.
            tempo_indication (TempoIndication): the tempo indication
            show_instrument_names (bool): if we want to show the instrument names next to the staffs
            show_bar_numbers  (bool): if we want to display all bar numbers
            show_tempo_indication (bool): if we want to display the tempo indication
            show_title (bool): if we want to show the title or not
        """
        super(VisualScoreTypeset, self).__init__(title, staffs, tempo_indication)
        self.show_instrument_names = show_instrument_names
        self.show_bar_numbers = show_bar_numbers
        self.show_tempo_indication = show_tempo_indication
        self.show_title = show_title

    def typeset(self):
        staffs = "\n".join(correct_indent(self._typeset_staff(staff), 20) for staff in self.staffs)

        layout = ''
        if not self.show_instrument_names:
            layout = 'indent = 0\mm'

        title = ' '
        if self.show_title:
            title = self._title

        typeset = r'''
            \score {{
                \header {{
                    piece = \markup {{ \fontsize #1 "{title}" }}
                    title = ""
                }}
                \new GrandStaff
                <<
                    {staffs}
                >>
                \layout {{
                    {layout}
                }}
            }}
        '''.format(title=title, staffs=staffs[20:], layout=layout)
        return LilypondScore(self._title, typeset)

    def _typeset_staff(self, staff, staff_options=None):
        parts = ['\\new Staff ']

        if staff_options:
            parts.append("\t" + ' \with {')
            parts.append("\t\t" + "\n\t\t".join(staff_options))
            parts.append("\t" + '}')

        parts.append('<<')

        parts.append(correct_indent(self._typeset_staff_options(staff), 8))
        parts.append("\t" + '{')
        parts.append("\t" + '\clef {}'.format(staff.clef))

        if self.show_instrument_names:
            parts.append("\t\t" + '\set Staff.instrumentName = #"{} "'.format(staff.instrument_name))

        parts.append(correct_indent(staff.music_expr, 12))

        parts.append("\t" + '}')
        parts.append('>>')
        return "\n".join(parts)

    def _typeset_staff_options(self, staff):
        barnumbers = ''
        if self.show_bar_numbers:
            barnumbers = '\\override Score.BarNumber.break-visibility = ##(#t #t #t)'

        tempo = ''
        if self.show_tempo_indication:
            tempo = '\\tempo ' + str(self.tempo_indication)

        return r'''
        {{
            {barnumbers}
            \key {key}
            \time {time}
            {tempo}
            \override Score.RehearsalMark.direction = #down
        }}'''.format(barnumbers=barnumbers, key=str(staff.key_signature),
                     time=str(staff.time_signature), tempo=tempo)


class MidiScoreTypeset(SimpleScoreTypeset):

    def __init__(self, title, staffs, tempo_indication):
        """The score typesetter for the midi output.

        Args:
            title (str): the title for this score
            staffs (list of TypesetStaffInfo): list of Staffs for each instrument.
            tempo_indication (TempoIndication): the tempo indication
        """
        super(MidiScoreTypeset, self).__init__(title, staffs, tempo_indication)

    def typeset(self):
        staffs = []
        for staff in self.staffs:
            staff_options = ['midiMinimumVolume = #{}'.format(staff.midi_options.min_volume),
                             'midiMaximumVolume = #{}'.format(staff.midi_options.max_volume),
                             'midiInstrument = #"{}" '.format(staff.midi_options.instrument)]
            staffs.append(correct_indent(self._typeset_staff(staff, staff_options), 20))

        typeset = r'''
            \score {{
                \unfoldRepeats
                \articulate
                \new GrandStaff
                <<
                    {staffs}
                >>
                \midi {{ }}
            }}
        '''.format(staffs="\n".join(staffs)[20:])

        return LilypondScore(self._title, typeset, is_midi_score=True)

    def _typeset_staff(self, staff, staff_options=None):
        options = ''
        if staff_options:
            options = r'''
                \with {{
                    {options}
                }}'''.format(options=correct_indent("\n".join(staff_options), 20)[20:])

        staff_settings = correct_indent(self._typeset_staff_options(staff), 8)

        typeset = correct_indent(r'''
            \new Staff
                {options}
            <<
                {staff_settings}
                {{
                    \clef {clef}
                    {music_expr}
                }}
            >>
        '''.format(options=correct_indent(options, 16), staff_settings=correct_indent(staff_settings, 16),
                   clef=staff.clef, music_expr=correct_indent(staff.music_expr, 20)[20:]), 12)
        return typeset

    def _typeset_staff_options(self, staff):
        return r'''
        {{
            \key {key}
            \time {time}
            \tempo {tempo}
            \override Score.RehearsalMark.direction = #down
        }}'''.format(key=str(staff.key_signature), time=str(staff.time_signature), tempo=str(self.tempo_indication))
