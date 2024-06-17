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
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('treble', 'piano_right_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('treble', 'piano_right_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('treble', 'piano_right_hand')}"
            }
        <<
            {
                \key c\major
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for synchronous_bar in composition_bars['treble'] }
                    \VAR{synchronous_bar.get_synchronous_bars()[0].get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('bass', 'piano_left_hand')}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('bass', 'piano_left_hand')}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('bass', 'piano_left_hand')}"
            }
        <<
            {
                \key c\major
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for synchronous_bar in composition_bars['bass'] }
                    \VAR{synchronous_bar.get_synchronous_bars()[0].get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
