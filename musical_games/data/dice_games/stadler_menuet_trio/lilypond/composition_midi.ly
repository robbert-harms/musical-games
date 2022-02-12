\version "2.19.81"
\include "articulate.ly"

% menuet with repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['menuet_treble_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['menuet_treble_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['menuet_treble_midi_settings'].instrument}"
            }
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
                        \VAR{game_mechanics.get_bar('menuet', 'piano_right_hand',  bar_nmrs['menuet']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{game_mechanics.get_bar('menuet', 'piano_right_hand',  bar_nmrs['menuet']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{render_settings['menuet_bass_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['menuet_bass_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['menuet_bass_midi_settings'].instrument}"
            }
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
		                \VAR{game_mechanics.get_bar('menuet', 'piano_left_hand',  bar_nmrs['menuet']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{game_mechanics.get_bar('menuet', 'piano_left_hand',  bar_nmrs['menuet']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}

% trio with repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['trio_treble_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['trio_treble_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['trio_treble_midi_settings'].instrument}"
            }
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
                        \VAR{game_mechanics.get_bar('trio', 'piano_right_hand',  bar_nmrs['trio']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{game_mechanics.get_bar('trio', 'piano_right_hand',  bar_nmrs['trio']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{render_settings['trio_bass_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['trio_bass_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['trio_bass_midi_settings'].instrument}"
            }
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
		                \VAR{game_mechanics.get_bar('trio', 'piano_left_hand',  bar_nmrs['trio']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{game_mechanics.get_bar('trio', 'piano_left_hand',  bar_nmrs['trio']['piano_left_hand'][bar_index])}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}

% menuet without repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['menuet_treble_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['menuet_treble_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['menuet_treble_midi_settings'].instrument}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(16) }
                    \VAR{game_mechanics.get_bar('menuet', 'piano_right_hand',  bar_nmrs['menuet']['piano_right_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{render_settings['menuet_bass_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['menuet_bass_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['menuet_bass_midi_settings'].instrument}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(16) }
                    \VAR{game_mechanics.get_bar('menuet', 'piano_left_hand',  bar_nmrs['menuet']['piano_left_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
