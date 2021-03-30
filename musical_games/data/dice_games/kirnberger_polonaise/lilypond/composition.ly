\version "2.19.81"
\include "articulate.ly"
\paper {
    print-all-headers = ##t
    score-markup-spacing = #'((basic-distance . 10))
    markup-system-spacing = #'((minimum-distance = 0))
    system-system-spacing = #'((basic-distance . 15))

    \BLOCK{ if render_options['large_page'] }
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
                    \VAR{composition.get_staff('polonaise', 'violin_1', bar_index)}
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
                    \VAR{composition.get_staff('polonaise', 'violin_2', bar_index)}
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
                        \VAR{composition.get_staff('polonaise', 'piano_right_hand', bar_index)}
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
                        \VAR{composition.get_staff('polonaise', 'piano_left_hand', bar_index)}
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
                midiMaximumVolume = #0.8624999999999999
                midiInstrument = #"Violin"
            }
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
                    \VAR{composition.get_staff('polonaise', 'violin_1', bar_index)}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition.get_staff('polonaise', 'violin_1', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #0.8624999999999999
                midiInstrument = #"violin"
            }
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
                    \VAR{composition.get_staff('polonaise', 'violin_2', bar_index)}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition.get_staff('polonaise', 'violin_2', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #0.85
                midiInstrument = #"acoustic grand"
            }
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
                    \VAR{composition.get_staff('polonaise', 'piano_right_hand', bar_index)}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition.get_staff('polonaise', 'piano_right_hand', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
        \new Staff
            \with {
                midiMinimumVolume = #0
                midiMaximumVolume = #0.6375
                midiInstrument = #"acoustic grand"
            }
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
                    \VAR{composition.get_staff('polonaise', 'piano_left_hand', bar_index)}
                \BLOCK{ endfor }
                % D.S. al fine
                \BLOCK{ for bar_index in range(2, 6) }
                    \VAR{composition.get_staff('polonaise', 'piano_left_hand', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
