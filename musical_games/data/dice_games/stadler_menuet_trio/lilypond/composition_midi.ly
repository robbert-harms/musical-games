\version "2.22.1"
\language "nederlands"
\include "articulate.ly"

% menuet with repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('menuet', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('menuet', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('menuet', 'piano_right_hand')}"
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

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('menuet', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('menuet', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('menuet', 'piano_left_hand')}"
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
		                \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
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
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('trio', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('trio', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('trio', 'piano_right_hand')}"
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

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('trio', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('trio', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('trio', 'piano_left_hand')}"
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
		                \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
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
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('menuet', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('menuet', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('menuet', 'piano_right_hand')}"
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
                    \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('menuet', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('menuet', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('menuet', 'piano_left_hand')}"
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
                    \VAR{composition_bars['menuet'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
