\version "2.22.1"
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
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
		                \BLOCK{ set bar = composition_bars['trio'][bar_index].get_bar('piano_left_hand') }
		                \BLOCK{ if bar.lilypond_str.startswith('\clef') }
                            \once \override Score.BreakAlignment #'break-align-orders = #(make-vector 3 '(span-bar breathing-sign staff-bar key clef time-signature))
                            \VAR{bar.lilypond_str}
                            \BLOCK{ if bar_index != 7 and not composition_bars['trio'][bar_index + 1].get_bar('piano_left_hand').lilypond_str.startswith('\clef') }
                                \once \override Score.BreakAlignment #'break-align-orders = #(make-vector 3 '(span-bar breathing-sign staff-bar key clef time-signature))
                                \once \override Staff.Clef.stencil = #(lambda (grob) (bracketify-stencil (ly:clef::print grob) Y 0.2 0.2 0.1))
                                \clef "bass"
                            \BLOCK{ endif }
                        \BLOCK{ else }
                        \VAR{bar.lilypond_str}
                        \BLOCK{endif}
    		        \BLOCK{ endfor }
	        	}
	        	\clef bass
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \BLOCK{ set bar = composition_bars['trio'][bar_index].get_bar('piano_left_hand') }
		                \BLOCK{ if bar.lilypond_str.startswith('\clef') }
		                    \once \override Score.BreakAlignment #'break-align-orders = #(make-vector 3 '(span-bar breathing-sign staff-bar key clef time-signature))
		                    \VAR{bar.lilypond_str}
                            \BLOCK{ if not composition_bars['trio'][bar_index + 1].get_bar('piano_left_hand').lilypond_str.startswith('\clef') }
                                \once \override Score.BreakAlignment #'break-align-orders = #(make-vector 3 '(span-bar breathing-sign staff-bar key clef time-signature))
                                \once \override Staff.Clef.stencil = #(lambda (grob) (bracketify-stencil (ly:clef::print grob) Y 0.2 0.2 0.1))
                                \clef "bass"
                            \BLOCK{ endif }
                        \BLOCK{ else }
                        \VAR{bar.lilypond_str}
                        \BLOCK{endif}
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
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 2/4
                \BLOCK{ for bar_index in range(16) }
                    \VAR{composition_bars['dance'][bar_index].get_bar('piano_left_hand').lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
