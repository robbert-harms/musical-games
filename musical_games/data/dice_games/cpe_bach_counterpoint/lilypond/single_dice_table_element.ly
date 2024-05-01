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
                \key c\major
            }
            {
                \clef \VAR{ table_name }
                \time 4/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bars()[0].lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
