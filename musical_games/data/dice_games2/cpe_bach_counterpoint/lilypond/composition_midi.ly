\version "2.19.81"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('treble', 0)}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('treble', 0)}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('treble', 0)}"
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
                \BLOCK{ for bar in composition_bars['treble'] }
                    \VAR{bar.lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{midi_settings.get_min_volume('bass', 0)}
                midiMaximumVolume = #\VAR{midi_settings.get_max_volume('bass', 0)}
                midiInstrument = #"\VAR{midi_settings.get_midi_instrument('bass', 0)}"
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
                \BLOCK{ for bar in composition_bars['bass'] }
                    \VAR{bar.lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}