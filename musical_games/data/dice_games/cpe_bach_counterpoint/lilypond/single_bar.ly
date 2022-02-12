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
                \key c\major
                \time 4/4
            }
            {
                \clef \VAR{ table_name }
                \BLOCK{ if table_name == 'treble' }
                    \VAR{ game_mechanics.bars[table_name]['piano_right_hand'][bar_nmr] }
                \BLOCK{ else }
                    \VAR{ game_mechanics.bars[table_name]['piano_left_hand'][bar_nmr] }
                \BLOCK{ endif }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
