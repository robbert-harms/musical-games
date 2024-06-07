\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 1600\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Scottish dance"
    composer = "Gerlach"
    tagline = ##f
}

\BLOCK{ include 'clef_changes.ly' }

\score {
    \header {
        piece = \markup { \fontsize #1 "Scottish dance & Trio" }
        composer = ""
        title = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key c \major
            }
            {
                \clef treble
                \time 2/4
                \BLOCK{ for bar_sequence in bar_collections['dance'].get_bar_sequences('piano_right_hand').values() }
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
                \key c \major
            }
            {
                \clef bass
                \time 2/4
                \BLOCK{ set loop_data = namespace(previous_bar=None) }
                \BLOCK{ for bar_ind, bar_sequence in bar_collections['dance'].get_bar_sequences('piano_left_hand').items() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \BLOCK{ if bar.get_annotation().has_clef_change }
                            \set Staff.forceClef = ##t
                            \VAR{bar.lilypond_str}
                        \BLOCK{ elif loop_data.previous_bar is not none and loop_data.previous_bar.get_annotation().has_clef_change }
                            \clefBracketed "bass"
                            \VAR{bar.lilypond_str}
                        \BLOCK{ else }
                            \VAR{bar.lilypond_str}
                        \BLOCK{endif}
                        \BLOCK{ set loop_data.previous_bar = bar }
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

