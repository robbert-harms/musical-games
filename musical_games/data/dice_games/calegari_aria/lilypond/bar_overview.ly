\version "2.22.1"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 1400\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Aria"
    composer = "Calegari"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "Primary bars" }
        title = ""
        composer = ""
    }
   <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Chant"
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \override Score.RehearsalMark.direction = #down
                \key f\major
            }
            {
                \clef treble
                \time 4/4
                \BLOCK{ for bar in bar_collections['part_one'].get_bars('chant').values() }
                    \VAR{bar.lilypond_str}
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
                    \override Score.RehearsalMark.direction = #down
                    \key f\major
                }
                {
                    \clef treble
                    \time 4/4
                    \BLOCK{ for bar in bar_collections['part_one'].get_bars('piano_right_hand').values() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
            \new Staff
            <<
                {
                    \override Score.BarNumber.break-visibility = ##(#t #t #t)
                    \override Score.RehearsalMark.direction = #down
                    \key f\major
                }
                {
                    \clef bass
                    \time 4/4
                    \BLOCK{ for bar in bar_collections['part_one'].get_bars('piano_left_hand').values() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
        >>
    >>
    \layout {
        indent = #0
    }
}
