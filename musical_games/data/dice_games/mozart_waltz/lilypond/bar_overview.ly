\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t

    \BLOCK{ if render_settings['single_page'] }
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
            }
            {
                \clef treble
                \time 3/8
                \BLOCK{ for bar_sequence in bar_collections['waltz'].get_bar_sequences('piano_right_hand').values() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
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
                \time 3/8
                \BLOCK{ for bar_sequence in bar_collections['waltz'].get_bar_sequences('piano_left_hand').values() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = #0
    }
}
