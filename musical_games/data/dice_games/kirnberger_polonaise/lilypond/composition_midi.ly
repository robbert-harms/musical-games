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
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('polonaise', 'violin_1')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('polonaise', 'violin_1')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('polonaise', 'violin_1')}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_1').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_1').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('polonaise', 'violin_2')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('polonaise', 'violin_2')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('polonaise', 'violin_2')}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_2').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_2').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('polonaise', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('polonaise', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('polonaise', 'piano_right_hand')}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('polonaise', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('polonaise', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('polonaise', 'piano_left_hand')}"
            }
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
