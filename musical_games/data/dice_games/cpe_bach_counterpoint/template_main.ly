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
    tagline = ""
}


\score {
    \header {
        piece = \markup { \fontsize #1 " " }
        title = ""
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
                e''8 [f''] g'' [f''] f'' [e''] e'' c''
                d''4 g' g''2
                g''8 [c''] b' c'' f''2
                f''4 e''8 [d''] e'' [g''] e'' c''
                d''4 g'' g' f''
                e''8 [d''] e'' d'' c''2 \bar "|."
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

                r4 e8 d c4 c'4
                c'4 b8 a b4 g
                a2 (a8) [b] c' d'
                g8 [g] a b c'4 c'4
                c'2 b4 a8 b
                c'1 \bar "|."
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}

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
                e''8 [f''] g'' [f''] f'' [e''] e'' c''
                d''4 g' g''2
                g''8 [c''] b' c'' f''2
                f''4 e''8 [d''] e'' [g''] e'' c''
                d''4 g'' g' f''
                e''8 [d''] e'' d'' c''2 \bar "|."
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

                r4 e8 d c4 c'4
                c'4 b8 a b4 g
                a2 (a8) [b] c' d'
                g8 [g] a b c'4 c'4
                c'2 b4 a8 b
                c'1 \bar "|."
            }
        >>
    >>
    \midi { }
}
