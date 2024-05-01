\version "2.22.1"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 420\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Counterpoint"
    composer = "C.P.E. Bach."
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key c\major
            }
            {
                \clef treble
                \time 4/4
                \BLOCK{ for bar in bar_collections['treble'].get_bars('piano_right_hand').values() }
                    \VAR{bar.lilypond_str}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key c\major
            }
            {
                \clef bass
                \time 4/4
                \BLOCK{ for bar in bar_collections['bass'].get_bars('piano_left_hand').values() }
                    \VAR{bar.lilypond_str}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = #0
    }
}

