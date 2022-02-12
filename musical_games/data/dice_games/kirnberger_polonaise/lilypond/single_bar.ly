\version "2.19.81"
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
                \time 3/4
            }
            {
                \clef treble
                \VAR{ game_mechanics.bars[table_name]['violin_1'][bar_nmr] }
                \bar "|."
            }
        >>
        \new Staff
        <<
            \set Staff.instrumentName = #"Violin #2 "
            {
                \key d\major
                \time 3/4
            }
            {
                \clef treble
                \VAR{ game_mechanics.bars[table_name]['violin_2'][bar_nmr] }
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
                }
                {
                    \clef treble
                    \VAR{ game_mechanics.bars[table_name]['piano_right_hand'][bar_nmr] }
                    \bar "|."
                }
            >>
            \new Staff
            <<
                {
                    \key d\major
                    \time 3/4
                }
                {
                    \clef bass
                    \VAR{ game_mechanics.bars[table_name]['piano_left_hand'][bar_nmr] }
                    \bar "|."
                }
            >>
        >>
    >>
}
