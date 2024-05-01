\version "2.22.1"
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
                \BLOCK{ if table_name == 'menuet' }
                    \key d\major
                \BLOCK{ else }
                    \key g\major
                \BLOCK{ endif }
            }
            {
                \clef treble
                \time 3/4
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \BLOCK{ if table_name == 'menuet' }
                    \key d\major
                \BLOCK{ else }
                    \key g\major
                \BLOCK{ endif }
            }
            {
                \clef bass
                \time 3/4
                \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
