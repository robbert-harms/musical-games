\version "2.22.1"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('waltz', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('waltz', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('waltz', 'piano_right_hand')}"
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
                        \VAR{composition_bars['waltz'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }

                \alternative { {\VAR{composition_bars['waltz'][7].get_bar('piano_right_hand').lilypond_str}} {\VAR{composition_bars['waltz'][7].get_bar('piano_right_hand').lilypond_str}} }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['waltz'][bar_index].get_bar('piano_right_hand').lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('waltz', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('waltz', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('waltz', 'piano_left_hand')}"
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
		                \VAR{composition_bars['waltz'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}

                \alternative { {\VAR{composition_bars['waltz'][7].get_bar('piano_left_hand').lilypond_str}} {\VAR{composition_bars['waltz'][7].get_bar('piano_left_hand_alternative').lilypond_str}} }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['waltz'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}
