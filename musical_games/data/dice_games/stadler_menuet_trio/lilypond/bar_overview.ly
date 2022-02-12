\version "2.19.81"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['large_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 2800\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Menuet and Trio"
    composer = "Stadler"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "Menuet" }
        composer = ""
        title = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\major
                \time 3/4
            }
            {
                \clef treble
                \BLOCK{ for bar in game_mechanics.bars['menuet']['piano_right_hand'].values() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\major
                \time 3/4
            }
            {
                \clef bass
                \BLOCK{ for bar in game_mechanics.bars['menuet']['piano_left_hand'].values() }
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
\score {
    \header {
        piece = \markup { \fontsize #1 "Trio" }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key g\major
                \time 3/4
            }
            {
                \clef treble
                \BLOCK{ for bar in game_mechanics.bars['trio']['piano_right_hand'].values() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key g\major
                \time 3/4
            }
            {
                \clef bass
                \BLOCK{ for bar in game_mechanics.bars['trio']['piano_left_hand'].values() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
