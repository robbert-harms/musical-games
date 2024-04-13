\version "2.19.81"
\paper {
	print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))

    \BLOCK{ if render_settings['single_page'] }
        paper-height = 360\mm  %% default is 297 for a4
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
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition_bars['menuet'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['menuet'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['menuet'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['menuet'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "Fine"}
            }
        >>
    >>
    \layout {
        indent = 0\mm
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
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition_bars['trio'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['trio'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['trio'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['trio'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "D.C. al Fine"}
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}

\BLOCK{ if render_settings['comment'] is not none }
    \markup {\fill-line \italic {"" "" "\VAR{ render_settings['comment'] }"}}
\BLOCK{ endif }
