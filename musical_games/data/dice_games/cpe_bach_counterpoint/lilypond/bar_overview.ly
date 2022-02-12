\version "2.19.81"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['large_page'] }
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
                \time 4/4
            }
            {
                \clef treble
                \BLOCK{ for bar_index, bar in game_mechanics.bars['treble']['piano_right_hand'].items() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key c\major
                \time 4/4
            }
            {
                \clef bass
                \BLOCK{ for bar_index, bar in game_mechanics.bars['bass']['piano_left_hand'].items() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = #0
    }
}

