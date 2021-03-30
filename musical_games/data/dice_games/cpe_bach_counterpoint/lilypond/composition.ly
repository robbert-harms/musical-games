\version "2.19.81"
\include "articulate.ly"
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
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(6) }
                    \VAR{composition.get_staff('treble', 'piano_right_hand', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
        <<
            {
                \key c\major
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(6) }
                    \VAR{composition.get_staff('bass', 'piano_left_hand',  bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}

\BLOCK{ if 'comment' in render_options }
    \markup {\fill-line \italic {"" "" "\VAR{ render_options['comment'] }"}}
\BLOCK{ endif }


\score {
    \unfoldRepeats
    \articulate
    \new GrandStaff
    <<
        \new Staff
            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #1
                midiInstrument = #"acoustic grand"
            }
        <<
            {
                \key c\major
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(6) }
                    \VAR{composition.get_staff('treble', 'piano_right_hand',  bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff

            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #0.75
                midiInstrument = #"acoustic grand"
            }
        <<
            {
                \key c\major
                \time 4/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(6) }
                    \VAR{composition.get_staff('bass', 'piano_left_hand', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
