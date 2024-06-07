\version "2.22.1"
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
                \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str }
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
                \VAR{ synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
