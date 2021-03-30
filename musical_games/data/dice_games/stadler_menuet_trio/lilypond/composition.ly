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
    title = "Menuet and Trio"
    composer = "Stadler"
    tagline = ##f
}
\score {
    \header {
        piece = \markup { \fontsize #1 "Menuet" }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition.get_staff('menuet', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('menuet', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
    		            \VAR{composition.get_staff('menuet', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('menuet', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "Fine"}
            }
        >>
    >>
    \layout {
        indent = 0\mm
    }
}

\score {
    \header {
        piece = \markup { \fontsize #1 "Trio" }
        title = ""
        composer = ""
    }
    \new PianoStaff
    <<
        \new Staff
        <<
            {
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition.get_staff('trio', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('trio', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
            }
        >>
        \new Staff
        <<
            {
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
    		            \VAR{composition.get_staff('trio', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('trio', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \once \override Score.RehearsalMark #'self-alignment-X = #right \mark \markup {\fontsize #-1 \italic "D.C. al Fine"}
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


%% the midi versions

% menuet with repeats
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
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition.get_staff('menuet', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('menuet', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
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
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
    		            \VAR{composition.get_staff('menuet', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('menuet', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}

% trio with repeats
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
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8) }
                        \VAR{composition.get_staff('trio', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
                \repeat volta 2{
                    \BLOCK{ for bar_index in range(8, 16) }
                        \VAR{composition.get_staff('trio', 'piano_right_hand', bar_index)}
                    \BLOCK{ endfor }
                }
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
                \key g\major
                \time 3/4
                \tempo 4 = 80
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
		        \repeat volta 2{
		            \BLOCK{ for bar_index in range(8) }
    		            \VAR{composition.get_staff('trio', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
		        \repeat volta 2{
    		        \BLOCK{ for bar_index in range(8, 16) }
    		            \VAR{composition.get_staff('trio', 'piano_left_hand', bar_index)}
    		        \BLOCK{ endfor }
	        	}
            }
        >>
    >>
    \midi { }
}

% menuet without repeats
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
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef treble
                \BLOCK{ for bar_index in range(16) }
                    \VAR{composition.get_staff('menuet', 'piano_right_hand', bar_index)}
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
                \key d\major
                \time 3/4
                \tempo 4 = 100
                \override Score.RehearsalMark.direction = #down
            }
            {
                \clef bass
                \BLOCK{ for bar_index in range(16) }
                    \VAR{composition.get_staff('menuet', 'piano_left_hand', bar_index)}
                \BLOCK{ endfor }
                \bar "|."
            }
        >>
    >>
    \midi { }
}
