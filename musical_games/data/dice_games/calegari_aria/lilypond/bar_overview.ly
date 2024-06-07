\version "2.22.1"
\language "nederlands"
\paper {
    print-all-headers = ##t
    \BLOCK{ if render_settings['single_page'] }
        system-system-spacing = #'((basic-distance . 15))
        paper-height = 3400\mm  %% default is 297 for a4
    \BLOCK{ endif }
}
\header{
    title = "Aria"
    composer = "Calegari"
    tagline = ##f
}

sopranovarCClef = {
    \set Staff.clefGlyph = "clefs.varC"
    \set Staff.clefPosition = 4
    \set Staff.middleCPosition = 4
    \set Staff.middleCClefPosition = 4
    \set Staff.clefPosition = -4
    \set Staff.middleCPosition = -6
}

\score {
    \header {
        piece = \markup { \fontsize #1 "Primary bars" }
        title = ""
        composer = ""
    }
   <<
        \new Staff
        <<
            \set Staff.instrumentName = #"Chant"
            {
                \override Score.BarNumber.break-visibility = ##(#t #t #t)
                \key g\major
                \sopranovarCClef
                \time 4/4
                \BLOCK{ for bar in bar_collections['part_one'].get_bars('chant').values() }
                    \set Score.currentBarNumber = #\VAR{loop.index} \VAR{bar.lilypond_str}
                \BLOCK{ endfor }
                \bar "|"
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
                    \BLOCK{ for bar in bar_collections['part_one'].get_bars('piano_right_hand').values() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
            \new Staff
            <<
                {
                    \key g\major
                    \clef bass
                    \time 4/4
                    \BLOCK{ for bar in bar_collections['part_one'].get_bars('piano_left_hand').values() }
                        \VAR{bar.lilypond_str}
                    \BLOCK{ endfor }
                    \bar "|"
                }
            >>
        >>
    >>
}
