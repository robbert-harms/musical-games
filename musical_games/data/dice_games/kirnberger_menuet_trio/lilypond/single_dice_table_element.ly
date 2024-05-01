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
                    \key d\minor
                \BLOCK{ endif }
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \BLOCK{ if table_name == 'menuet' }
                    \key d\major
                \BLOCK{ else }
                    \key d\minor
                \BLOCK{ endif }
            }
            {
                \clef bass
                \time 3/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
