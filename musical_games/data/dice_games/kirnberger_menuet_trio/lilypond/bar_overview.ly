\version "2.19.81"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_options['large_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 1400\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Menuet and Trio"
    composer = "Kirnberger"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "Menuet" }
        title = ""
        composer = ""
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
                \BLOCK{ for bar in dice_game.bars['menuet']['piano_right_hand'].values() }
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
                \BLOCK{ for bar in dice_game.bars['menuet']['piano_left_hand'].values() }
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
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\minor
                \time 3/4
            }
            {
                \clef treble
                \BLOCK{ for bar in dice_game.bars['trio']['piano_right_hand'].values() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\minor
                \time 3/4
            }
            {
                \clef bass
                \BLOCK{ for bar in dice_game.bars['trio']['piano_left_hand'].values() }
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
