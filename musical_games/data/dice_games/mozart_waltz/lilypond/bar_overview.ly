\version "2.19.81"
\paper {
    print-all-headers = ##t

    \BLOCK{ if render_settings['large_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 1200\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Waltz"
    composer = "Mozart"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "" }
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
                \time 3/8
            }
            {
                \clef treble
                \BLOCK{ for bar in game_mechanics.bars['waltz']['piano_right_hand'].values() }
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
                \time 3/8
            }
            {
                \clef bass
                \BLOCK{ for ind, bar in game_mechanics.bars['waltz']['piano_left_hand'].items() }
                    \BLOCK{ if game_mechanics.bars['waltz']['piano_left_hand_alternative'][ind] }
                        << {\voiceOne \VAR{bar} } \new Voice { \voiceTwo \VAR{game_mechanics.bars['waltz']['piano_left_hand_alternative'][ind]}} >>
                    \BLOCK{ else }
                        \VAR{bar}
                    \BLOCK{ endif }
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = #0
    }
}
