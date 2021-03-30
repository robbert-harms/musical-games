\version "2.19.81"
\include "articulate.ly"
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
    title = "Waltz"
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
                \time 3/8
                \tempo 8 = 110
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(7) }
                        \VAR{composition.get_staff('waltz', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }

                \alternative { {\VAR{composition.get_staff('waltz', 'piano_right_hand', 7)}} {\VAR{composition.get_staff('waltz', 'piano_right_hand', 7)}} }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('waltz', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key c\major
                \time 3/8
                \tempo 8 = 110
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(7) }
    		            \VAR{composition.get_staff('waltz', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}

                \alternative { {\VAR{composition.get_staff('waltz', 'piano_left_hand', 7)}} {\VAR{composition.get_staff('waltz', 'piano_left_hand_alternative', 7)}} }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('waltz', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}

\BLOCK{ if 'comment' in render_options }
    \markup {\fill-line \italic {"" "" "\VAR{ render_options['comment'] }"}}
\BLOCK{ endif }


\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #1
                midiInstrument = #"acoustic grand"
            }
        <<
            {
                \key c\major
                \time 3/8
                \tempo 8 = 110
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(7) }
                        \VAR{composition.get_staff('waltz', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }

                \alternative { {\VAR{composition.get_staff('waltz', 'piano_right_hand', 7)}} {\VAR{composition.get_staff('waltz', 'piano_right_hand', 7)}} }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('waltz', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #0.75
                midiInstrument = #"acoustic grand"
            }
        <<
            {
                \key c\major
                \time 3/8
                \tempo 8 = 110
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(7) }
    		            \VAR{composition.get_staff('waltz', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}

                \alternative { {\VAR{composition.get_staff('waltz', 'piano_left_hand', 7)}} {\VAR{composition.get_staff('waltz', 'piano_left_hand_alternative', 7)}} }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('waltz', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}
