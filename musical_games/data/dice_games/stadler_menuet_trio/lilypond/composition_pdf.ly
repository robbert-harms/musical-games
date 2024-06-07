\version "2.22.1"
\language "nederlands"
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
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 3/4
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key d\major
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 3/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
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
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 3/4
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }
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
                \time 3/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
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
    \BLOCK{ if '\n' in render_settings['comment'] }
    \BLOCK{ for line in render_settings['comment'].split('\n') }
        \markup {\fill-line \italic {"" "" "\VAR{ line }"}}
    \BLOCK{ endfor }
    \BLOCK{ else }
        \markup {\fill-line \italic {"" "" "\VAR{ render_settings['comment'] }"}}
    \BLOCK{ endif }
\BLOCK{ endif }
