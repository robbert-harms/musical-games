\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t

    \BLOCK{ if render_settings['single_page'] }
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
                \override Score.RehearsalMark.direction = #down
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['polonaise'].get_bar_sequences('violin_1').values() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|"
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \override Score.RehearsalMark.direction = #down
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_sequence in bar_collections['polonaise'].get_bar_sequences('violin_2').values() }
                    \BLOCK{ for bar in bar_sequence.get_bars() }
                        \VAR{bar.lilypond_str}
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
                    \override Score.BarNumber.break-visibility = ##(#t #t #t)
                    \override Score.RehearsalMark.direction = #down
                    \key d\major
                }
                {
                    \clef treble
                    \time 3/4
                    \BLOCK{ for bar_sequence in bar_collections['polonaise'].get_bar_sequences('piano_right_hand').values() }
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
                    \override Score.RehearsalMark.direction = #down
                    \key d\major
                }
                {
                    \clef bass
                    \time 3/4
                    \BLOCK{ for bar_sequence in bar_collections['polonaise'].get_bar_sequences('piano_left_hand').values() }
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

