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
                \key c\major
            }
            {
                \clef \VAR{ table_name }
                \time 4/4
                \VAR{ synchronous_bar_sequence.get_synchronous_bars()[0].get_bars()[0].lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
