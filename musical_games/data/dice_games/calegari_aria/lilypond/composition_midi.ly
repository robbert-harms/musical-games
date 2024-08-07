\version "2.22.1"
\language "nederlands"
\include "articulate.ly"
\score {
    \articulate
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('part_one', 'chant')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('part_one', 'chant')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('part_one', 'chant')}"
            }
        <<
            {
                \key g\major
                \time 4/4
                \tempo 4 = 80
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('chant').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "."
                \BLOCK{ for bar_index in range(10) }
                    \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('chant').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('part_one', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('part_one', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('part_one', 'piano_right_hand')}"
            }
        <<
            {
                \key g\major
                \time 4/4
                \tempo 4 = 80
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "."
                \BLOCK{ for bar_index in range(10) }
                    \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('piano_right_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('part_one', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('part_one', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('part_one', 'piano_left_hand')}"
            }
        <<
            {
                \key g\major
                \time 4/4
                \tempo 4 = 80
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(8) }
                    \BLOCK{for bar in composition_bars['part_one'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "."
                \BLOCK{ for bar_index in range(10) }
                    \BLOCK{for bar in composition_bars['part_two'][bar_index].get_bar_sequence('piano_left_hand').get_bars()}
                        \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
