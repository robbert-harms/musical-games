\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))
    system-system-spacing = #'((basic-distance . 15))

    \BLOCK{ if render_settings['single_page'] }
        paper-height = 400\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Aria"
    composer = "Calegari"
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
            \set Staff.instrumentName = #"Chant"
            {
                \key g\major
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 4/4
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('chant').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "."
                \BLOCK{ for bar_index in range(10) }
                    \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('chant').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new PianoStaff
        <<
            \set PianoStaff.instrumentName = #"Piano"
            \new Staff
            <<
                {
                    \key g\major
                    \tempo 4 = 80
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef treble
                    \time 4/4
                    \BLOCK{ for bar_index in range(8) }
                        \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                    \bar "."
                    \BLOCK{ for bar_index in range(10) }
                        \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key g\major
                    \tempo 4 = 80
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef bass
                    \time 4/4
                    \BLOCK{ for bar_index in range(8) }
                        \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                    \bar "."
                    \BLOCK{ for bar_index in range(10) }
                        \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
        >>
    >>
}

\BLOCK{ if render_settings['comment'] is not none }
    \BLOCK{ if '\n' in render_settings['comment'] }
    \BLOCK{ for line in render_settings['comment'].split('\n') }
        \markup {\fill-line \italic {"" "" "\VAR{ line }"}}
    \BLOCK{ endfor }
    \BLOCK{ else }
        \markup {\fill-line \italic {"" "" "\VAR{ render_settings['comment'] }"}}
    \BLOCK{ endif }
\BLOCK{ endif }
