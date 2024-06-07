\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
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
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['menuet'].get_bar_sequences('piano_right_hand').values() }
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
                \key d\major
            }
            {
                \clef bass
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['menuet'].get_bar_sequences('piano_left_hand').values() }
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
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['trio'].get_bar_sequences('piano_right_hand').values() }
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
                \key g\major
            }
            {
                \clef bass
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['trio'].get_bar_sequences('piano_left_hand').values() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
