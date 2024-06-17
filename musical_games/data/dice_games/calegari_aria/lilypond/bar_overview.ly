\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 3700\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Aria"
    composer = "Calegari"
    tagline = ##f
}

#(add-new-clef "sopranovarC" "clefs.varC" -4 0 0)

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
                \key g\major
                \clef sopranovarC
                \time 4/4
                \BLOCK{ for bar_sequence in bar_collections['part_one'].get_bar_sequences('chant').values() }
                    \BLOCK{ set bar_index = loop.index }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \set Score.currentBarNumber = #\VAR{bar_index} \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
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
                    \key g\major
                    \clef treble
                    \time 4/4
                    \BLOCK{ for bar_sequence in bar_collections['part_one'].get_bar_sequences('piano_right_hand').values() }
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
                    \key g\major
                    \clef bass
                    \time 4/4
                    \BLOCK{ for bar_sequence in bar_collections['part_one'].get_bar_sequences('piano_left_hand').values() }
                        \BLOCK{ for bar in bar_sequence.get_bars() }
                            \VAR{bar.lilypond_str}
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
        >>
    >>
}
