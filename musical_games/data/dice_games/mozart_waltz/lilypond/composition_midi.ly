\version "2.19.81"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['piano_rh_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['piano_rh_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['piano_rh_midi_settings'].instrument}"
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
                        \VAR{game_mechanics.get_bar('waltz', 'piano_right_hand',  bar_nmrs['waltz']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }

                \alternative { {\VAR{game_mechanics.get_bar('waltz', 'piano_right_hand', bar_nmrs['waltz']['piano_right_hand'][7])}} {\VAR{game_mechanics.get_bar('waltz', 'piano_right_hand', bar_nmrs['waltz']['piano_right_hand'][7])}} }

                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{game_mechanics.get_bar('waltz', 'piano_right_hand',  bar_nmrs['waltz']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{render_settings['piano_lh_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['piano_lh_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['piano_lh_midi_settings'].instrument}"
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
		                \VAR{game_mechanics.get_bar('waltz', 'piano_left_hand',  bar_nmrs['waltz']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}

                \alternative { {\VAR{game_mechanics.get_bar('waltz', 'piano_left_hand', bar_nmrs['waltz']['piano_left_hand'][7])}} {\VAR{game_mechanics.get_bar('waltz', 'piano_left_hand_alternative', bar_nmrs['waltz']['piano_left_hand'][7])}} }

		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{game_mechanics.get_bar('waltz', 'piano_left_hand',  bar_nmrs['waltz']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}
