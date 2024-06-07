\version "2.19.81"
\language "nederlands"
\paper {
    print-all-headers = ##f
    paper-height = 50\mm
    paper-width = 100\mm
}
\header{
    title = ""
    tagline = ##f
}

\BLOCK{ include 'clef_changes.ly' }

\score {
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c \major
            }
            {
                \clef treble
                \time 2/4
                \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c \major
            }
            {
                \BLOCK{ if synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars()[0].get_annotation().clef == 'treble' }
                    \bassToTreble
                \BLOCK{ elif synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars()[0].get_annotation().clef == 'bass' }
                    \bassToBass
                \BLOCK{ else }
                    \bass
                \BLOCK{ endif }
                \time 2/4
                \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
