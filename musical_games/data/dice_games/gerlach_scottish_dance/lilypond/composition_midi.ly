\version "2.19.81"
\include "articulate.ly"

% dance with repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('dance', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('dance', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('dance', 'piano_right_hand')}"
            }
        <<
            {
                \key c \major
                \time 2/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
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

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('dance', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('dance', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('dance', 'piano_left_hand')}"
            }
        <<
            {
                \key c \major
                \time 2/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
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
                \key c \major
                \time 2/4
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

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('trio', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('trio', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('trio', 'piano_left_hand')}"
            }
        <<
            {
                \key c \major
                \time 2/4
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
            }
        >>
    >>
    \midi { }
}

% dance without repeats
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('dance', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('dance', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('dance', 'piano_right_hand')}"
            }
        <<
            {
                \key c \major
                \time 2/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(16) }
                    \VAR{composition_bars['dance'][bar_index].get_bar('piano_right_hand').lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('dance', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('dance', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('dance', 'piano_left_hand')}"
            }
        <<
            {
                \key c \major
                \time 2/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(16) }
                    \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
