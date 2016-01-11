from musical_games.dice_games.lilypond.base import LilypondScore, MusicBookComment, LilypondBook
from musical_games.dice_games.lilypond.staff_layouts import AutoLayout, StaffInfo
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

    def __init__(self, title, staffs, tempo_indication, staff_layout=None, show_bar_numbers=False,
                 show_tempo_indication=True, show_title=True):
        """Information of a single piece for use in the MusicBook typesetter.

        Args:
            title (str): the title for this score
            staffs (list of TypesetStaffInfo): list of Staffs for each instrument.
            tempo_indication (TempoIndication): the tempo indication
            staff_layout (StaffLayout): the layout mechanism for displaying the staffs
            show_bar_numbers  (bool): if we want to display all bar numbers
            show_tempo_indication (bool): if we want to display the tempo indication
            show_title (bool): if we want to show the title or not
        """
        super(VisualScoreTypeset, self).__init__(title, staffs, tempo_indication)
        self.staff_layout = staff_layout or AutoLayout()
        self.show_bar_numbers = show_bar_numbers
        self.show_tempo_indication = show_tempo_indication
        self.show_title = show_title

    def typeset(self):
        staff_infos = [self._get_staff_info(staff) for staff in self.staffs]
        staff = self.staff_layout.typeset_staffs(staff_infos)

        title = ' '
        if self.show_title:
            title = self._title

        typeset = r'''
            \score {{
                \header {{
                    piece = \markup {{ \fontsize #1 "{title}" }}
                    title = ""
                }}

                {staff}
            }}
        '''.format(title=title, staff=staff)

        return LilypondScore(self._title, typeset)

    def _get_staff_info(self, staff):
        options_block = correct_indent(self._typeset_staff_options(staff), 0)
        parts = ['{',
                 " "*4 + '\clef {}'.format(staff.clef),
                 correct_indent(staff.music_expr, 4),
                 '}']
        return StaffInfo('\n'.join(parts), staff.instrument_name, options_block=options_block)

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

    def __init__(self, title, staffs, tempo_indication, midi_options=None):
        """The score typesetter for the midi output.

        Args:
            title (str): the title for this score
            staffs (list of TypesetStaffInfo): list of Staffs for each instrument.
            tempo_indication (TempoIndication): the tempo indication
            midi_options (list): if set, a list with additional midi options per tract
        """
        super(MidiScoreTypeset, self).__init__(title, staffs, tempo_indication)
        self._midi_options = midi_options

    def typeset(self):
        staffs = []
        midi_instrument_names = []

        for ind, staff in enumerate(self.staffs):
            instrument_name = self._get_midi_option(ind, 'instrument')

            midi_instrument_names.append(instrument_name)

            staff_options = ['midiMinimumVolume = #{}'.format(self._get_midi_option(ind, 'min_volume')),
                             'midiMaximumVolume = #{}'.format(self._get_midi_option(ind, 'max_volume')),
                             'midiInstrument = #"{}" '.format(instrument_name)]
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

        return LilypondScore(self._title, typeset, is_midi_score=True, midi_instruments=midi_instrument_names)

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

    def _get_midi_option(self, staff_ind, option_key):
        if self._midi_options and len(self._midi_options) > staff_ind:
            option = getattr(self._midi_options[staff_ind], option_key)
            if option is not None:
                return option
        return getattr(self.staffs[staff_ind].midi_options, option_key)
