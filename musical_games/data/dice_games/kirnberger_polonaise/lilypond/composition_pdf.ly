\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))
    system-system-spacing = #'((basic-distance . 15))

    \BLOCK{ if render_settings['single_page'] }
        paper-height = 410\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Polonaise"
    composer = "Kirnberger"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        title = ""
        composer = ""
    }
    <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #1 "
            {
                \key d\major
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_1').get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \key d\major
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 3/4
                \BLOCK{ for bar_index in range(14) }
                    \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('violin_2').get_bars()[0].lilypond_str}
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
                    \tempo 4 = 70
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef treble
                    \time 3/4
                    \BLOCK{ for bar_index in range(14) }
                        \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_right_hand').get_bars()[0].lilypond_str}
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key d\major
                    \tempo 4 = 70
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef bass
                    \time 3/4
                    \BLOCK{ for bar_index in range(14) }
                        \VAR{composition_bars['polonaise'][bar_index].get_bar_sequence('piano_left_hand').get_bars()[0].lilypond_str}
                        \BLOCK{ if bar_index == 1}
                            \mark \markup { \musicglyph #"scripts.segno" }
                        \BLOCK{ elif bar_index == 5 }
                            \bar "||"
                            \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "Fine"}
                        \BLOCK{ endif }
                    \BLOCK{ endfor }
                    \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "D.S. al Fine"}
                    \bar "|."
                }
            >>
        >>
    >>
}

\BLOCK{ if render_settings['comment'] is not none }
    \BLOCK{ if '\n' in render_settings['comment'] }
    \BLOCK{ for line in render_settings['comment'].split('\n') }
        \markup {\fill-line \italic {"" "" "\VAR{ line }"}}
    \BLOCK{ endfor }
    \BLOCK{ else }
        \markup {\fill-line \italic {"" "" "\VAR{ render_settings['comment'] }"}}
    \BLOCK{ endif }
\BLOCK{ endif }
