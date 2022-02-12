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
                \time 3/8
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
                \key c\major
                \time 3/8
            }
            {
                \clef bass
                \BLOCK{ if game_mechanics.bars['waltz']['piano_left_hand_alternative'][bar_nmr] }
                    << {\voiceOne \VAR{ game_mechanics.bars['waltz']['piano_left_hand'][bar_nmr] } } \new Voice { \voiceTwo \VAR{ game_mechanics.bars['waltz']['piano_left_hand_alternative'][bar_nmr] }} >>
                \BLOCK{ else }
                    \VAR{ game_mechanics.bars['waltz']['piano_left_hand'][bar_nmr] }
                \BLOCK{ endif }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = #0
    }
}
