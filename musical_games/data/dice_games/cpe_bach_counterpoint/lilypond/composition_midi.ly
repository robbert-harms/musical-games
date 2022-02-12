\version "2.19.81"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings.treble_midi_settings.min_volume}
                midiMaximumVolume = #\VAR{render_settings.treble_midi_settings.max_volume}
                midiInstrument = #"\VAR{render_settings.treble_midi_settings.instrument}"
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
                \BLOCK{ for bar_index in range(6) }
                    \VAR{game_mechanics.get_bar('treble', 'piano_right_hand',  bar_nmrs['treble']['piano_right_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #\VAR{render_settings.bass_midi_settings.min_volume}
                midiMaximumVolume = #\VAR{render_settings.bass_midi_settings.max_volume}
                midiInstrument = #"\VAR{render_settings.bass_midi_settings.instrument}"
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
                \BLOCK{ for bar_index in range(6) }
                    \VAR{game_mechanics.get_bar('bass', 'piano_left_hand',  bar_nmrs['bass']['piano_left_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
