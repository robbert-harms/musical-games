\version "2.22.1"
\language "nederlands"
\include "articulate.ly"

\BLOCK{ include 'clef_changes.ly' }

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
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 2/4
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(4) }
                        \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(4, 8) }
                        \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
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
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(4) }
		                \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
    		        \BLOCK{ endfor }
	        	}
	        	\clef bass
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(4, 8) }
    		            \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
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
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 2/4
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(4) }
                        \BLOCK{for bar in composition_bars['trio'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(4, 8) }
                        \BLOCK{for bar in composition_bars['trio'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
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
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(4) }
                        \BLOCK{for bar in composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
                    \BLOCK{ endfor }
	        	}
	        	\clef bass
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(4, 8) }
                        \BLOCK{for bar in composition_bars['trio'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                            \VAR{ bar.lilypond_str }
                        \BLOCK{ endfor }
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
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 2/4
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
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
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['dance'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
