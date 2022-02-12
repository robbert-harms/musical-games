\version "2.19.81"
\include "articulate.ly"
\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['violin_1_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['violin_1_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['violin_1_midi_settings'].instrument}"
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
                    \VAR{game_mechanics.get_bar('polonaise', 'violin_1',  bar_nmrs['polonaise']['violin_1'][bar_index])}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{game_mechanics.get_bar('polonaise', 'violin_1',  bar_nmrs['polonaise']['violin_1'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['violin_2_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['violin_2_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['violin_2_midi_settings'].instrument}"
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
                    \VAR{game_mechanics.get_bar('polonaise', 'violin_2',  bar_nmrs['polonaise']['violin_2'][bar_index])}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{game_mechanics.get_bar('polonaise', 'violin_2',  bar_nmrs['polonaise']['violin_2'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['piano_rh_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['piano_rh_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['piano_rh_midi_settings'].instrument}"
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
                    \VAR{game_mechanics.get_bar('polonaise', 'piano_right_hand',  bar_nmrs['polonaise']['piano_right_hand'][bar_index])}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{game_mechanics.get_bar('polonaise', 'piano_right_hand',  bar_nmrs['polonaise']['piano_right_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #\VAR{render_settings['piano_lh_midi_settings'].min_volume}
                midiMaximumVolume = #\VAR{render_settings['piano_lh_midi_settings'].max_volume}
                midiInstrument = #"\VAR{render_settings['piano_lh_midi_settings'].instrument}"
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
                    \VAR{game_mechanics.get_bar('polonaise', 'piano_left_hand',  bar_nmrs['polonaise']['piano_left_hand'][bar_index])}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{game_mechanics.get_bar('polonaise', 'piano_left_hand',  bar_nmrs['polonaise']['piano_left_hand'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
