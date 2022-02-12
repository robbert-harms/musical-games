\version "2.19.81"
\paper {
    print-all-headers = ##t

    \BLOCK{ if render_settings['large_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 3400\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Polonaise"
    composer = "Kirnberger"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        title = ""
        composer = ""
    }
    <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #1 "
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\major
                \time 3/4
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index, bar in game_mechanics.bars['polonaise']['violin_1'].items() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key d\major
                \time 3/4
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index, bar in game_mechanics.bars['polonaise']['violin_2'].items() }
                    \VAR{bar}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new PianoStaff
        <<
            \set PianoStaff.instrumentName = #"Piano"
            \new Staff
            <<
                {
                    \override Score.BarNumber.break-visibility = ##(#t #t #t)
                    \key d\major
                    \time 3/4
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef treble
                    \BLOCK{ for bar_index, bar in game_mechanics.bars['polonaise']['piano_right_hand'].items() }
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
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef bass
                    \BLOCK{ for bar_index, bar in game_mechanics.bars['polonaise']['piano_left_hand'].items() }
                        \VAR{bar}
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
        >>
    >>
}

