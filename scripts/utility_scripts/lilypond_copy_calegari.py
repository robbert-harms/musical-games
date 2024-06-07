__author__ = 'Robbert Harms'
__date__ = '2024-04-29'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import re
from pathlib import Path

from musical_games.dice_games.base import SimpleBarCollection, SimpleBar
from musical_games.dice_games.data_csv import SimpleBarCollectionCSVWriter

chant = r"""
\set Score.currentBarNumber = #1 e''8.( c''16) c''8.( a'16) a'8[ b'8] c''8 d''8
| \set Score.currentBarNumber = #2 c''4. d''16[ e''16] d''4 b'8.\noBeam b'16
| \set Score.currentBarNumber = #3 e'4.( fis'16) [ g'16 ] fis'4 a'8. [ d''16 ]
| \set Score.currentBarNumber = #4 \partial 2. <d' d''>4 r4 r4
| \set Score.currentBarNumber = #5 fis'4. fis'8 \grace { fis'8 } e'8[ d'8] e'8 fis'8
| \set Score.currentBarNumber = #6 a'4.( b'16) c''16 b'4 b'8.\noBeam g'16
| \set Score.currentBarNumber = #7 \partial 2. g'4 r4 r4
| \set Score.currentBarNumber = #8 a'4 d''8. c''16 b'4 d''16[ b'16] c''16 d''16
| \set Score.currentBarNumber = #9 a'8[ d''8] cis''8[ b'8 ] a'8[ b'8] cis''8[ e''8 ]
| \set Score.currentBarNumber = #10 c''4. a'8 b'4 d''8.\noBeam b'16
| \set Score.currentBarNumber = #11 a'4.\fermata b'8 a'4 d''8.\noBeam d''16
| \set Score.currentBarNumber = #12 a'4. b'16 c''16 b'4 g''8. d''16
| \set Score.currentBarNumber = #13 a'4 a'16( [ b'16 c''16 a'16 ] ) g'4 d''8.\noBeam d''16
| \set Score.currentBarNumber = #14 \partial 2. g'4 r4 r4
| \set Score.currentBarNumber = #15 a'4. b'16 [ c''16 ] b'4 d''8.\noBeam [ d''16 ]
| \set Score.currentBarNumber = #16 d''4 \times 2/3 { b'8 [ g'8 e'8 ] } d'4 \grace { fis'16 } e'8.\noBeam [ d'16 ]
| \set Score.currentBarNumber = #17 c''4.( e''16) d''16 c''4 a'8.\noBeam d''16
| \set Score.currentBarNumber = #18 g'8 [ fis'8] g'8[ a'8 ] b'8[ g'8] b'8[ c''8 ]
| \set Score.currentBarNumber = #0 \partial 4 d''8.( d''16)
| \set Score.currentBarNumber = #19 fis''4. d''8 \grace{c''8} b'4 a'8 gis'8
| \set Score.currentBarNumber = #20 e''8[ g''8] fis''8[ e''8] d''8[ c''8] b'8[ a'8]
| \set Score.currentBarNumber = #21 e''4( e''16) d''16 c''16 b'16 a'4 a'8.\noBeam d''16
| \set Score.currentBarNumber = #22 \partial 2. \grace{a'4} g'2 r4
| \set Score.currentBarNumber = #23 g'4 b'8.( a'16) g'4 g'4
| \set Score.currentBarNumber = #24 cis''8 [ d''8] e''8[ d''8 ] g''8 [ d''8] b'8[ fis'8 ]
| \set Score.currentBarNumber = #0 \partial 4 d''8. d''16
| \set Score.currentBarNumber = #25 c''4( a'8)\noBeam e''8 e''4( d''8) c''8
| \set Score.currentBarNumber = #26 d''4. cis''8 c''8[ a'8] b'8 g'8]
| \set Score.currentBarNumber = #27 b'4. e''8 \grace { d''8 } cis''4 b'8 [ cis''8 ]
| \set Score.currentBarNumber = #28 a'4 d'4 b'8.( g'16) c''8.( a'16)
| \set Score.currentBarNumber = #29 d''16 [ e''16 d''16 c''16 ] b'8 [ b'8 ] b'16 [ c''16 b'16 a'16 ] g'8 [ b'8 ]
| \set Score.currentBarNumber = #0 \partial 4 d''8.\noBeam ( d''16)
| \set Score.currentBarNumber = #30 e''4. e''8 c''4 b'4
"""

piano_right_hand = r"""
<c'' e''>4 <a' c''>4 <fis' a'>2
r4 <fis' e''>4( <g' d''>8) <g' b'>8[ <g' b'>8 <g' b'>8 ]
r4 <e' g'>4 <d' fis'>8 [ <fis' a'>8] <fis' a'>8 <a' d''>8
\partial 2. r4 <fis'' a'>4 <d'' fis'>4
<d' fis'>4 <d' fis'>4 <a e'>4 <a e'>4
a'8( d'8) <a' c''>8( d'8) <g' b'>8( d'8) <g' b'>8( d'8)
\partial 2. g'4 <d' b'>4 <b g'>4
{<<{\voiceOne a'2( b'4) <g' d''>4} \new Voice {\voiceTwo r4 d'2.}>>}
a'8 [ d''8 cis''8 b'8 ] a'4 r8 <fis' d''>8
<a' c''>8[ d'8] <fis' a'>8[ d'8 ] <g' b'>8[ d'8] <b' d''>8[ <g' b'>8 ]
<fis' a'>2.\fermata r4
<a' c''>2( <g' b'>8) <b' d''>8[ <b' d''>8 <b' d''>8]
\times 2/3 { c'8 [ d'8 a'8 ] } \times 2/3 { c'8 [ d'8 a'8 ] } \times 2/3 { b8 [ d'8 g'8 ] } \times 2/3 { g'8 [ b'8 d''8 ] }
\partial 2. g'8.[ b'16 d''8. g''16] g'4
{<<{\voiceOne a'2 b'4 r4} \new Voice {\voiceTwo r4 d'2.}>>}
<fis' d''>4 <g' b'>8. [ <e' g'>16 ] <d' fis'>4 <cis' e'>4
<e' c''>2 <a' c''>4 <d' a'>4 \break
<b g'>4. <d' a'>8 <g' b'>4. <a' c''>8
\partial 4 r4
r4 <f' f''>4\f r4 <gis' b'>4\p
<g' e''>8\f [ <e'' g''>8 <d'' fis''>8 <c'' e''>8] <b' d''>8[ <a' c''>8 <g' b'>8 <fis' a'>8]
<e' c'' e''>2 r8 d'16[ fis'16 a'8 d''8]
\partial 2. \grace{<c' a'>4} <b g'>2 r4
\times 2/3 { b8 d'8 g'8} \times 2/3 { b8 d'8 g'8} \times 2/3 { b8 d'8 g'8} \times 2/3 { b8 d'8 g'8}
r4 <g' b' d''>4 r4 <d' g' b'>4
\partial 4 <d' fis' a' d''>4
\times 2/3 {r8 a'8[ c''8]} \times 2/3 {e''8 c''8 a'8} \times 2/3 {r8 fis'8 a'8} \times 2/3 {d''8 a'8 fis'8}
{<<{\voiceOne d''4 cis''4 c''4 b'4} \new Voice {\voiceTwo <e' g'>2 d'2}>>}
r4 e''2 cis''4
r4 <d' fis' a' d''>4 <g' b'>4 <a' c''>4
<a' d''>4 r4 <d' b'>4 r4
\partial 4 <fis' d''>4
{<<{\voiceOne e''2 c''4 b'4} \new Voice {\voiceTwo g'8 gis'8 a'2 d'4}>>}
"""

piano_left_hand = r"""
<c, c>2 <d, d>2
r4 <c c'>4( <b, b>8) r8 g4
cis2 d4 d,4
\partial 2. <d, d>2 r4
<d fis>4 <d fis>4 <a, e>4 <a, e>4
fis4 d4 g4 g,4
\partial 2. <g b>4 r4 r4
{<<{\voiceOne a8[ b8 a8 g8 ] fis4 r8 d8} \new Voice {\voiceTwo d2. r4}>>}
<d, d>2 g4 g,4
<d d,>2 g4 g,4
<d, d>2.\fermata r4
r8 a8[ fis8 d8] g4 g,4
<fis, fis>2 <g, g>4 <b, b>4
\partial 2. <g b>2.
fis4 d4 g4 g,4
b4 g4 a4 a,4
r8. c16 [ c'8. a16 ] fis2 \break
g4. fis8 e4. c8
\partial 4 r4
<d, d>2 <e, e>2
c4. c'8 d'4 d4
r8 c'16 [ b16 c'8 a8 ] fis2
\partial 2. r8. g16[ d8. b,16] g,4
<g, g>1
g4 r4 g,4 r4
\partial 4 <d, d>4
<c c'>2 <d d'>2
<e, e>2 <fis, fis>4 <g, g>4
<g, g>2 <a, a>2
<d, d>2 r2
g4 r4 g,4 r4
\partial 4 <d' d>4
<d d'>4 <c c'>8 a8 fis8 d8 g8 g,8
"""

chant_bars = chant.split('\n')
right_hand_bars = piano_right_hand.split('\n')
left_hand_bars = piano_left_hand.split('\n')

sync_bars = {}
anacrusis = None
for ind, (chant_bar, piano_right_hand_bar, piano_left_hand_bar) in enumerate(zip(chant_bars[1:-1],
                                                                             right_hand_bars[1:-1],
                                                                             left_hand_bars[1:-1])):
    match = re.search(r'Score\.currentBarNumber = #(\d+)', chant_bar)
    bar_index = int(match.groups()[0])

    chant_bar_clean = chant_bar[match.end()+1:]

    if bar_index == 0:
        anacrusis = {'chant': SimpleBar(chant_bar_clean),
                     'piano_right_hand': SimpleBar(piano_right_hand_bar),
                     'piano_left_hand': SimpleBar(piano_left_hand_bar)}
    elif anacrusis is not None:
        
        anacrusis = None
    else:
        sync_bars[bar_index] = {'chant': SimpleBar(chant_bar_clean),
                                'piano_right_hand': SimpleBar(piano_right_hand_bar),
                                'piano_left_hand': SimpleBar(piano_left_hand_bar)}

a = SimpleBarCollection(sync_bars)

writer = SimpleBarCollectionCSVWriter()
# writer.write_csv(a, Path('/home/robbert/programming/python/musical-games/musical_games/data/dice_games/gerlach_scottish_dance/scottish_dance_bars2.csv'))

print()
