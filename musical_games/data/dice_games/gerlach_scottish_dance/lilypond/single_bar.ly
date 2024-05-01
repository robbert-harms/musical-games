\version "2.19.81"
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
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c \major
            }
            {
                \BLOCK{ if synchronous_bar.get_bar('piano_left_hand').lilypond_str.startswith('\clef "treble"') }
                    \bassToTreble
                \BLOCK{ elif synchronous_bar.get_bar('piano_left_hand').lilypond_str.startswith('\clef "bass"') }
                    \bassToBass
                \BLOCK{ else }
                    \bass
                \BLOCK{ endif }
                \time 2/4
                \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
