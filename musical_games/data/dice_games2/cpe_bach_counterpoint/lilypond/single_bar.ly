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
                \clef \VAR{ clef }
                \VAR{ bar.lilypond_str }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
