\version "2.22.1"
\language "nederlands"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('contredanse', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('contredanse', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('contredanse', 'piano_right_hand')}"
            }
        <<
            {
                \key c\major
                \time 2/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(7) }
                        \VAR{composition_bars['contredanse'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }

                \alternative {
                    {\VAR{composition_bars['contredanse'][7].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}}
                    {\VAR{composition_bars['contredanse'][7].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}}
                }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition_bars['contredanse'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('contredanse', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('contredanse', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('contredanse', 'piano_left_hand')}"
            }
        <<
            {
                \key c\major
                \time 2/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(7) }
		                \VAR{composition_bars['contredanse'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}

                \alternative {
                    {\VAR{split_voices(composition_bars['contredanse'][7].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str)[0]}}
                    {\VAR{split_voices(composition_bars['contredanse'][7].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str)[1]}}
                }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['contredanse'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}
