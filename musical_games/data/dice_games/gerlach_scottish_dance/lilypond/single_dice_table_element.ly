\version "2.22.1"
\paper {
    print-all-headers = ##f
    paper-height = 50\mm
    paper-width = 100\mm
}
\header{
    title = ""
    tagline = ##f
}

\BLOCK{ include 'clef_changes.ly' }

\score {
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c \major
            }
            {
                \clef treble
                \time 2/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c \major
            }
            {
                \BLOCK{ if synchronous_bars|length > 0 and synchronous_bars[0].get_bar('piano_left_hand').get_annotation().clef == 'treble' }
                    \bassToTreble
                \BLOCK{ elif synchronous_bars|length > 0 and synchronous_bars[0].get_bar('piano_left_hand').get_annotation().clef == 'bass' }
                    \bassToBass
                \BLOCK{ else }
                    \clef bass
                \BLOCK{ endif }
                \time 2/4

                \BLOCK{ for synchronous_bar in synchronous_bars }
                \BLOCK{ set bar = synchronous_bar.get_bar('piano_left_hand') }
                \BLOCK{ set has_next = loop.index0 != synchronous_bars|length - 1 }
                \BLOCK{ if has_next }
                \BLOCK{ set next_bar = synchronous_bars[loop.index0 + 1].get_bar('piano_left_hand') }
                \BLOCK{ endif }
                \BLOCK{ if bar.get_annotation().has_clef_change }
                    \set Staff.forceClef = ##t
                    \VAR{ bar.lilypond_str }
                    \BLOCK{ if has_next and not next_bar.get_annotation().has_clef_change }
                       \clefAfterBarOnce \clefBracketed "bass"
                    \BLOCK{ endif }
                \BLOCK{ else }
                    \VAR{ bar.lilypond_str }
                \BLOCK{endif}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}
