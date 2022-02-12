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
                \BLOCK{ if table_name == 'menuet' }
                    \key d\major
                    \time 3/4
                \BLOCK{ else }
                    \key g\major
                    \time 3/4
                \BLOCK{ endif }
            }
            {
                \clef treble
                \VAR{ game_mechanics.bars[table_name]['piano_right_hand'][bar_nmr] }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \BLOCK{ if table_name == 'menuet' }
                    \key d\major
                    \time 3/4
                \BLOCK{ else }
                    \key g\major
                    \time 3/4
                \BLOCK{ endif }
            }
            {
                \clef bass
                \VAR{ game_mechanics.bars[table_name]['piano_left_hand'][bar_nmr] }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
