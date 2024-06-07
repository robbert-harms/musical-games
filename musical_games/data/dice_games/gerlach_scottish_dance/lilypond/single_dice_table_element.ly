\version "2.22.1"
\language "nederlands"
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
                \BLOCK{ for bar in synchronous_bar_sequence.get_bar_sequence('piano_right_hand').get_bars() }
                \VAR{ bar.lilypond_str }
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
                \BLOCK{ set bars = synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars() }
                \BLOCK{ if bars|length > 0 and bars[0].get_annotation().clef == 'treble' }
                    \bassToTreble
                \BLOCK{ elif bars|length > 0 and bars[0].get_annotation().clef == 'bass' }
                    \bassToBass
                \BLOCK{ else }
                    \clef bass
                \BLOCK{ endif }
                \time 2/4

                \BLOCK{ for bar in bars }
                \BLOCK{ set has_next = loop.index0 != bars|length - 1 }
                \BLOCK{ if has_next }
                \BLOCK{ set next_bar = bars[loop.index0 + 1] }
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
