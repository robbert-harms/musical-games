\version "2.19.81"
\paper {
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))
    system-system-spacing = #'((basic-distance . 15))

    \BLOCK{ if render_settings['large_page'] }
        paper-height = 370\mm  %% default is 297 for a4
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
                \time 3/4
                \tempo 4 = 70
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(14) }
                    \VAR{game_mechanics.get_bar('polonaise', 'violin_1',  bar_nmrs['polonaise']['violin_1'][bar_index])}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
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
                    \time 3/4
                    \tempo 4 = 70
                    \override Score.RehearsalMark.direction = #down
                }
                {
                    \clef treble
                    \BLOCK{ for bar_index in range(14) }
                        \VAR{game_mechanics.get_bar('polonaise', 'piano_right_hand',  bar_nmrs['polonaise']['piano_right_hand'][bar_index])}
                    \BLOCK{ endfor }
                    \bar "|."
                }
            >>
            \new Staff
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
    \markup {\fill-line \italic {"" "" "\VAR{ render_settings['comment'] }"}}
\BLOCK{ endif }
