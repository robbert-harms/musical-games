\version "2.19.81"
\paper {
    print-all-headers = ##f
    paper-height = 50\mm
    paper-width = 100\mm
}
\header{
    title = ""
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "" }
        title = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c\major
                \time 2/4
            }
            {
                \clef treble
                \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c\major
                \time 2/4
            }
            {
                \clef bass
                \BLOCK{ if synchronous_bar.get_bar('piano_left_hand_alternative').lilypond_str != '' }
                    <<{\voiceOne \VAR{synchronous_bar.get_bar('piano_left_hand').lilypond_str}} \new Voice {\voiceTwo \VAR{synchronous_bar.get_bar('piano_left_hand_alternative').lilypond_str}}>>
                \BLOCK{ else }
                    \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                \BLOCK{ endif }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = #0
    }
}
