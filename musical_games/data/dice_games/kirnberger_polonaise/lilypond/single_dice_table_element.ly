\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##f
    paper-height = 100\mm
    paper-width = 150\mm
}
\header{
    title = ""
    tagline = ##f
}
\score {
    <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #1 "
            {
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \VAR{ synchronous_bar_sequence.get_bar_sequence('violin_1').get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \VAR{ synchronous_bar_sequence.get_bar_sequence('violin_2').get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
        \new PianoStaff
        <<
            \set PianoStaff.instrumentName = #"Piano"
            \new Staff
            <<
                {
                    \key d\major
                }
                {
                    \clef treble
                    \time 3/4
                    \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key d\major
                }
                {
                    \clef bass
                    \time 3/4
                    \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str }
                    \bar "|."
                }
            >>
        >>
    >>
}
