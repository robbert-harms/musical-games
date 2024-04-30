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
\score {
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c \major
                \time 2/4
            }
            {
                \clef treble
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c \major
                \time 2/4
            }
            {
                \clef bass
                \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
