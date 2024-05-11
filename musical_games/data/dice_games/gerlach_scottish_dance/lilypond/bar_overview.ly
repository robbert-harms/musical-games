\version "2.22.1"
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
                \BLOCK{ for bar in bar_collections['dance'].get_bars('piano_right_hand').values() }
                    \VAR{bar.lilypond_str}
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
                \BLOCK{ for bar_ind, bar in bar_collections['dance'].get_bars('piano_left_hand').items() }
                    \BLOCK{ if bar.lilypond_str.startswith('\clef "treble"') or bar.lilypond_str.startswith('\clefBracketed "treble"')}
                        \set Staff.forceClef = ##t
                        \VAR{bar.lilypond_str}
                        \BLOCK{ if not bar_collections['dance'].get_bars('piano_left_hand')[bar_ind + 1].lilypond_str.startswith('\clef') }
                            \clefBracketed "bass"
                        \BLOCK{ endif }
                    \BLOCK{ elif bar.lilypond_str.startswith('\clef "bass"') }
                        \set Staff.forceClef = ##t
                        \VAR{bar.lilypond_str}
                    \BLOCK{ else }
                    \VAR{bar.lilypond_str}
                    \BLOCK{endif}
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
    >>
    \layout {
        indent = #0
    }
}

