\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##f
    paper-height = 100\mm
    paper-width = 150\mm
}
\header{
    title = ""
    tagline = ##f
}

#(add-new-clef "sopranovarC" "clefs.varC" -4 0 0)

\score {
    <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Chant"
            {
                \key g\major
                \clef sopranovarC
                \time 4/4
                \BLOCK{ for bar in synchronous_bar_sequence.get_bar_sequence('chant').get_bars() }
                \VAR{ bar.lilypond_str }
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
                    \key g\major
                    \clef treble
                    \time 4/4
                    \BLOCK{ for bar in synchronous_bar_sequence.get_bar_sequence('piano_right_hand').get_bars() }
                    \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key g\major
                    \clef bass
                    \time 4/4
                    \BLOCK{ for bar in synchronous_bar_sequence.get_bar_sequence('piano_left_hand').get_bars() }
                    \VAR{ bar.lilypond_str }
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
        >>
    >>
}
