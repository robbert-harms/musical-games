\version "2.22.1"
\paper {
	print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))

    \BLOCK{ if render_settings['single_page'] }
        paper-height = 360\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Scottish Dance - Dance and Trio"
    composer = "Gerlach"
    tagline = ##f
}

\BLOCK{ include 'clef_changes.ly' }

\score {
    \header {
        piece = \markup { \fontsize #1 "Scottish Dance" }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c \major
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 2/4
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition_bars['dance'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['dance'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key c \major
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
	        	\clef bass
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
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
                \key c \major
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 2/4
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
                \key c \major
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
		        \repeat volta 2{
		            \BLOCK{ set loop_data = namespace(previous_bar=None) }
		            \BLOCK{ for bar_index in range(8) }
		                \BLOCK{ set bar = composition_bars['trio'][bar_index].get_bar('piano_left_hand') }
		                \BLOCK{ if bar.get_annotation().has_clef_change }
                            \clefAfterBarOnce
                            \set Staff.forceClef = ##t
                            \VAR{bar.lilypond_str}
                        \BLOCK{ elif loop_data.previous_bar is not none
                                        and loop_data.previous_bar.get_annotation().has_clef_change
                                        and loop_data.previous_bar.get_annotation().clef == 'treble' }
                            \set Staff.forceClef = ##t \clefAfterBarOnce \clefBracketed "bass"
                            \VAR{bar.lilypond_str}
                        \BLOCK{ else }
                            \VAR{bar.lilypond_str}
                        \BLOCK{endif}
                        \BLOCK{ set loop_data.previous_bar = bar}
    		        \BLOCK{ endfor }
	        	}
	        	\clef bass
		        \repeat volta 2{
		            \BLOCK{ set loop_data = namespace(previous_bar=None) }
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \BLOCK{ set bar = composition_bars['trio'][bar_index].get_bar('piano_left_hand') }
		                \BLOCK{ if bar.get_annotation().has_clef_change }
                            \clefAfterBarOnce
                            \set Staff.forceClef = ##t
                            \VAR{bar.lilypond_str}
                        \BLOCK{ elif loop_data.previous_bar is not none
                                        and loop_data.previous_bar.get_annotation().has_clef_change
                                        and loop_data.previous_bar.get_annotation().clef == 'treble' }
                            \set Staff.forceClef = ##t \clefAfterBarOnce \clefBracketed "bass"
                            \VAR{bar.lilypond_str}
                        \BLOCK{ else }
                            \VAR{bar.lilypond_str}
                        \BLOCK{endif}
                        \BLOCK{ set loop_data.previous_bar = bar}
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
