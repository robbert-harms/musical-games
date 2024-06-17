\version "2.22.1"
\language "nederlands"
\paper {
	page-count = 1
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))

    scoreTitleMarkup = \markup {
        \override #'(baseline-skip . 10) %% changes the distance between title/subtitle and composer/arranger
        \column {
            \override #'(baseline-skip . 3.5)
            \column {
                \huge \larger \bold
                \fill-line {
                    \larger \fromproperty #'header:title
                }
                \fill-line {
                    \large \smaller \bold
                    \larger \fromproperty #'header:subtitle
                }
                \fill-line {
                    \smaller \bold
                    \fromproperty #'header:subsubtitle
                }
            }
            \override #'(baseline-skip . 3.5)
            \column {
                \fill-line {
                    \fromproperty #'header:poet
                    { \large \bold \fromproperty #'header:instrument }
                    \fromproperty #'header:composer
                }
                \fill-line {
                    \fromproperty #'header:piece
                    \fromproperty #'header:meter
                    \fromproperty #'header:arranger
                }
            }
        }
    }
}
\header{
    title = "Counterpoint"
    composer = "C.P.E. Bach."
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key c\major
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \time 4/4
                \BLOCK{ for synchronous_bar in composition_bars['treble'] }
                    \VAR{synchronous_bar.get_synchronous_bars()[0].get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c\major
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \time 4/4
                \BLOCK{ for synchronous_bar in composition_bars['bass'] }
                    \VAR{synchronous_bar.get_synchronous_bars()[0].get_bars()[0].lilypond_str}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
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
