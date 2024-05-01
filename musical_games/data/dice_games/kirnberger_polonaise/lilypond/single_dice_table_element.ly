\version "2.22.1"
\paper {
    print-all-headers = ##f
    paper-height = 100\mm
    paper-width = 150\mm
}
\header{
    title = ""
    tagline = ##f
}
\score {
    \new PianoStaff
    <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #1 "
            {
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bar('violin_1').lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \key d\major
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for synchronous_bar in synchronous_bars }
                \VAR{ synchronous_bar.get_bar('violin_2').lilypond_str }
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new PianoStaff
        <<
            \set PianoStaff.instrumentName = #"Piano"
            \new Staff
            <<
                {
                    \key d\major
                }
                {
                    \clef treble
                    \time 3/4
                    \BLOCK{ for synchronous_bar in synchronous_bars }
                    \VAR{ synchronous_bar.get_bar('piano_right_hand').lilypond_str }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key d\major
                }
                {
                    \clef bass
                    \time 3/4
                    \BLOCK{ for synchronous_bar in synchronous_bars }
                    \VAR{ synchronous_bar.get_bar('piano_left_hand').lilypond_str }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
        >>
    >>
}
