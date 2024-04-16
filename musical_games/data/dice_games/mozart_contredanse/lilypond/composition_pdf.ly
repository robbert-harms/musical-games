\version "2.19.81"
\paper {
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))
    system-system-spacing = #'((basic-distance . 15))

    scoreTitleMarkup = \markup {
        \override #'(baseline-skip . 10) %% changes the distance between title/subtitle and composer/arranger
        \column {
            \override #'(baseline-skip . 3.5)
            \column {
                \huge \larger \bold
                \fill-line {
                    \larger \fromproperty #'header:title
                }
                \fill-line {
                    \large \smaller \bold
                    \larger \fromproperty #'header:subtitle
                }
                \fill-line {
                    \smaller \bold
                    \fromproperty #'header:subsubtitle
                }
            }
            \override #'(baseline-skip . 3.5)
            \column {
                \fill-line {
                    \fromproperty #'header:poet
                    { \large \bold \fromproperty #'header:instrument }
                    \fromproperty #'header:composer
                }
                \fill-line {
                    \fromproperty #'header:piece
                    \fromproperty #'header:meter
                    \fromproperty #'header:arranger
                }
            }
        }
    }
}
\header{
    title = "Contredanse"
    composer = "Mozart"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        composer = ""
        title = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c\major
                \time 2/4
                \tempo 8 = 120
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(7) }
                        \VAR{composition_bars['contredanse'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }

                \alternative { {\VAR{composition_bars['contredanse'][7].get_bar('piano_right_hand').lilypond_str}} {\VAR{composition_bars['contredanse'][7].get_bar('piano_right_hand').lilypond_str}} }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['contredanse'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key c\major
                \time 2/4
                \tempo 8 = 120
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(7) }
		                \VAR{composition_bars['contredanse'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}

                \alternative { {\VAR{composition_bars['contredanse'][7].get_bar('piano_left_hand').lilypond_str}} {\VAR{composition_bars['contredanse'][7].get_bar('piano_left_hand_alternative').lilypond_str}} }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['contredanse'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
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

