__author__ = 'Robbert Harms'
__date__ = '2024-04-29'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.base import SimpleBarCollection, SimpleBar
from musical_games.dice_games.data_csv import SimpleBarCollectionCSVWriter

piano_right_hand_voice_1 = r"""\stemDown d''16 [\stemDown e''16 \stemDown f''16 \stemDown d''16] \stemDown b'8 [\stemDown d''8]
\stemDown a''16 [\stemDown gis''16 \stemDown a''16 \stemDown b''16] \stemDown c'''8 [\stemDown d'''8]
\stemDown <c'' g''>8 [\stemDown <c'' fis''>8] <b' g''>4
\stemDown g'8 [\stemDown c''16 \stemDown d''16] \stemDown e''16 [\stemDown f''16 \stemDown g''8]
\stemDown e''8. [\stemDown d''16] \stemDown b'8 [\stemDown b'8]
\stemDown cis''16 [\stemDown cis''16 \stemDown e''16 \stemDown cis''16] \stemDown a'8 [\stemDown e''8]
\stemDown c''8 [\stemDown <g' e''>8] <e' c''>4
\stemDown c''8 [\stemDown c''16 \stemDown b'16] \stemUp a'8 [\stemUp e'8]
\stemDown b'8 [\stemDown a''8] \stemDown g''8 [\stemDown f''8]
\stemUp b'8 [\stemUp g'8] g''4
\stemDown f''16 [\stemDown e''16 \stemDown f''16 \stemDown a''16] \stemDown f''8 [\stemDown b'8]
\stemDown <e'' g''>8 [\stemDown <g' c''>8] <c'' e''>4
<a' c''>4 <g' cis''>4
\stemDown e''16 [\stemDown d''16 \stemDown cis''16 \stemDown e''16] d''4
\stemUp <e' g'>8 [\stemUp <f' a'>16 \stemUp <e' g'>16] \stemUp <e' g'>8 [\stemUp <e' c''>8]
\stemDown g''16 [\stemDown a''16 \stemDown b''16 \stemDown c'''16] \stemDown d'''8 [\stemDown g''8]
\stemDown e''8 [\grace { \stemUp d''8 } \stemDown e''8] e'4
\stemDown d'''16 [\stemDown cis'''16 \stemDown d'''16 \stemDown e'''16] \stemDown f'''8 [\stemDown a''8]
\stemDown d'''8 [\stemDown a''8] \stemDown b''8 [\stemDown e'''8]
\stemDown g''16 [\stemDown fis''16 \stemDown fis''16 \stemDown e'''16] \stemDown e'''16 [\stemDown d'''16 \stemDown c'''16 \stemDown a''16]
\stemDown e''8 [\stemDown d''8] \stemDown a''16 [\stemDown g''16 \stemDown f''16 \stemDown d''16]
\stemDown c'''8 [\stemDown d'''16 \stemDown es'''16] \stemDown g''8 [\stemDown e''8]
\stemDown e''8 [\stemDown b'8] \stemDown gis''8 [\stemDown e''8]
\stemDown c'''8 [\stemDown bes''8] \stemDown g''8 [\stemDown e''8]
\stemDown e''8 [\stemDown c''8] \stemDown g''8 [\stemDown e''8]
\stemDown a'8 [\stemDown c''8] \stemDown e''8 [\stemDown a''8]
\stemDown c''8 [\stemDown e''8] \stemDown a''8 [\stemDown c'''8]
\stemDown e''8 [\stemDown d''8] c''4
\stemDown d''8 [\stemDown e''16 \stemDown d''16] \stemDown a'8 [\stemDown f''8]
\stemUp e''8 [\stemUp c'''8] g''4
\stemDown f''16 [\stemDown e''16 \stemDown dis''16 \stemDown e''16] \stemDown c'''8 [\stemDown e''8]
<g' c'' e''>4 <g' b' d''>8 r8
\stemDown g''8 [\stemDown b'8] \stemDown fis''8 [\stemDown a'8]
\stemDown a''8 [\stemDown <c'' a''>8] <a' a''>4
\stemDown c''16 [\stemDown d''16 \stemDown e''16 \stemDown c''16] \stemDown a'8 [\stemDown a''8]
\stemDown a''8 [\stemDown f''8] \stemDown d''8 [\stemDown c''8]
\stemDown a''16 [\stemDown f''16 \stemDown e''16 \stemDown d''16] \stemDown c''16 [\stemDown g''16 \stemDown b'16 \stemDown d''16]
\stemDown f''16 [\stemDown e''16 \stemDown f''16 \stemDown g''16] \stemDown a''8 [\stemDown a''8]
\stemUp e''8 [\stemUp f''16 \stemUp e''16] \stemUp dis''8 [\stemUp e''8]
\stemUp <e' g'>8 [\stemUp <f' a'>16 \stemUp <e' g'>16] \stemDown <e' c''>8 [\stemDown <c'' e''>8]
\stemUp gis'16 [\stemUp a'16 \stemUp b'16 \stemUp gis'16] \stemUp e'8 [\stemUp e''8]
\stemDown a''8 [\stemDown gis''16 \stemDown a''16] \stemDown bes''8 [\stemDown a''8]
\stemDown a'8 [\stemDown bes'16 \stemDown b'16] \tuplet 3/2 {\stemDown c''8 [\stemDown f''8 \stemDown a'8]}
\stemDown c'''8 [\stemDown d''8] \stemDown b''8 [\stemDown d''8]
\stemDown b'8 [\stemDown d''8] \stemDown g''8 [\stemDown b''8]
\stemDown c''8 [\stemDown e''8] g'4
\stemDown c''8 [\stemDown e''8] g''4
\stemDown <gis' d''>8 [\stemDown <gis' e''>8] \stemDown <a' fis''>8 [\stemDown <b' gis''>8]
\stemDown b''16 [\stemDown c'''16 \stemDown d'''16 \stemDown b''16] \stemDown g''8 [\stemDown f'''8]
\stemUp c''8 [\stemUp <e' c''>8] <e' c''>4
\stemDown c''8 [\stemDown <g' e''>8] <e' c''>4
\stemDown c''8 [\stemDown c'''8] c''4
\stemDown f''8 [\stemDown a''8] f''4
\stemUp b''8 [\stemUp d'''16 \stemUp b''16] \stemUp a''8 [\stemUp gis''8]
\stemUp d''8 [\stemUp e''16 \stemUp d''16] \stemUp d''8 [\stemUp g''8]
\stemDown a''8 [\stemDown e''8] \stemDown cis'''8 [\stemDown e'''8]
\stemDown bes'8 [\stemDown c''16 \stemDown e''16] g''4
\stemDown g''8 [\stemDown d'''16 \stemDown dis'''16] \stemDown e'''8 [\stemDown g''8]
\stemDown c''16 [\stemDown d''16 \stemDown e''16 \stemDown d''16] c''4
\stemDown a'8 [\stemDown d''16 \stemDown e''16] \stemDown f''16 [\stemDown g''16 \stemDown a''8]
\stemDown b''8 [\stemDown f''16 \stemDown b''16] \stemDown d'''8 [\stemDown f'''8]
\stemDown g''8 [\stemDown fis''16 \stemDown g''16] \stemDown as''8 [\stemDown f''16 \stemDown d''16]
\stemDown c'''8 [\stemDown a''8] \stemDown f'''8 [\stemDown a''8]
\stemDown f''8 [\stemDown <c'' a''>8] <a' f''>4
\stemUp e'8 [\stemUp c''16 \stemUp e'16] \stemDown g'8 [\stemDown e''8]
\stemDown g''16 [\stemDown f''16 \stemDown f''16 \stemDown d'''16] \stemDown d'''8 [\stemDown f''8]
\stemDown c'''8 [\stemDown d'''16 \stemDown e'''16] \stemDown f'''8 [\stemDown a''8]
\stemDown d'''8 [\stemDown c'''8] \stemDown bes''8 [\stemDown a''8]
\stemDown c'''16 [\stemDown bes''16 \stemDown a''16 \stemDown g''16] \stemDown a''8 [\stemDown f''8]
\stemDown g''8 [\stemDown <b' g''>8] <b' g''>4
\stemDown d''8 [\stemDown e''16 \stemDown d''16] \stemDown c'''8 [\stemDown a''8]
\stemDown a''8 [\stemDown f''16 \stemDown d''16] \stemDown c''16 [\stemDown g''16 \stemDown b'16 \stemDown d''16]
\stemDown a''16 [\stemDown b''16 \stemDown c'''16 \stemDown d'''16] \stemDown e'''8 [\stemDown gis''8]
\stemDown d'''8 [\stemDown c'''8] \stemDown a''8 [\stemDown e''8]
\stemDown e''8 [\stemDown e''16 \stemDown d''16] \stemDown a''8 [\stemDown d''8]
\stemDown a''16 [\stemDown gis''16 \stemDown a''16 \stemDown b''16] c'''4
\stemUp <e' c''>8 [\stemUp <e' c''>8] \stemUp <f' d''>8 [\stemUp <g' e''>8]
\stemDown e''16 [\stemDown d''16 \stemDown cis''16 \stemDown d''16] \stemDown a''8 [\stemDown d''8]
\stemDown c''8 [\stemDown a'8] \stemDown a''8 [\stemDown e''8] |
\stemDown a''16 [\stemDown g''16 \stemDown f''16 \stemDown e''16] \stemDown f''8 [\stemDown d''8]
\stemDown c'''16 [\stemDown d'''16 \stemDown e'''16 \stemDown f'''16] \stemDown g'''8 [\stemDown c'''8]
\grace { \stemUp ais''8 } b''4 \grace { \stemUp ais''8 } \stemDown b''8 [\stemDown e'''8]
a''2
\stemDown c''8 [\stemDown e''8] \stemDown a'8 [\stemDown a''8]
\stemUp d''16 [\stemUp cis''16 \stemUp d''16 \stemUp e''16] \stemUp f''8 [\stemUp d''8]
\stemDown c'''8 [\stemDown a''8] \stemDown b''8 [\stemDown c'''8]
\stemUp <e' g'>8 [\stemUp <f' a'>16 \stemUp <e' g'>16] \stemUp <e' g'>8 [\stemUp <g' e''>8]
\stemDown e''8 [\stemDown e''16 \stemDown d''16] \stemDown c''8 [\stemDown a'8]
\stemDown <c'' c'''>8 [\stemDown <g'' b''>16 \stemDown <f'' a''>16] \stemDown <e'' g''>8 [\stemDown <f'' a''>8]
\stemDown e'''8 [\stemDown c'''8] \stemDown g''8 [\stemDown e''8]
\stemDown g''8 [\stemDown b'8] c''4
\stemDown fis''16 [\stemDown g''16 \stemDown a''16 \stemDown fis''16] \stemDown d''8 [\stemDown c'''8]
\stemDown b''8 [\stemDown e''8] \stemDown e'''8 [\stemDown e''8]
\stemDown g''8 [\stemDown c''8] \stemDown e''8 [\stemDown c'''8]
\stemUp e''16 [\stemUp f''16 \stemUp d''16 \stemUp e''16] c''4
\stemDown a''16 [\stemDown g''16 \stemDown fis''16 \stemDown g''16] \stemDown c'''8 [\stemDown e''8]
\stemDown f''8 [\stemDown a''8] c''4
\stemDown <e'' g''>8 [\stemDown <c'' e''>8] <e'' c'''>4
\stemUp a''8. \turn [\stemUp b''16] \stemUp c'''8 [\stemUp e''8]
\stemDown e''8 [\stemDown c''8] \stemDown a''8 [\stemDown g''8]
\stemDown <g' c'' g''>8 [\stemDown <g' c''>8] \stemDown <a' c'' f''>8 [\stemDown <c'' f'' a''>8]
\stemUp c''8 [\stemUp <e' c''>8] <e' c''>4
\stemDown b''8 [\stemDown d'''16 \stemDown b''16] \stemDown a''8 [\stemDown gis''8]
\stemDown g''16 [\stemDown f''16 \stemDown e''16 \stemDown d''16] \stemDown c''8 [\stemDown b'8]
\stemDown a'8 [\stemDown d''8] \stemDown cis''16 [\stemDown d''16 \stemDown e''16 \stemDown d''16]
\stemDown gis''8 [\stemDown e''8] \stemDown a''8 [\stemDown e''8]
\stemDown g''16 [\stemDown fis''16 \stemDown g''16 \stemDown gis''16] \stemDown a''8 [\stemDown d''8]
\stemDown a''16 [\stemDown gis''16 \stemDown a''16 \stemDown b''16] \stemDown c'''8 [\stemDown a''8]
\stemUp f''8. \turn [\stemUp g''16] a''4
\stemUp a''8 [\stemUp g''8] \stemUp fis''8 [\stemUp g''8]
\stemDown b''8 [\stemDown e'''16 \stemDown d'''16] \stemDown c'''8 [\stemDown a''8]
\stemDown b''8 [\stemDown e''8] \stemDown dis''16 [\stemDown e''16 \stemDown d''16 \stemDown b'16]
\stemDown e''8 [\stemDown c''8] \stemDown a''8 [\stemDown e''8]
\stemDown b''8 [\stemDown d'''16 \stemDown f'''16] \stemDown e'''8 [\stemDown gis''8]
\grace { \stemUp a''8 } bes''4 \grace { \stemUp a''8 } \stemDown bes''8 [\stemDown g''8]
\stemUp a''8. [\stemUp g''16] \stemUp f''8 [\stemUp f''8]
\stemDown f''8 [\stemDown g'16 \stemDown b'16] \stemDown d''8 [\stemDown a''8]
\stemDown e''8. [\stemDown f''16] \stemDown e''8 [\stemDown d''8]
\stemDown f'''8 [\stemDown e'''8] \stemDown c'''8 [\stemDown a''8]
\stemUp a'8 [\stemUp <c' a'>8] <c' a'>4
\stemDown a'8 [\stemDown f''8] \stemDown as'16 [\stemDown f''16 \stemDown g'16 \stemDown g''16]
d''4 r4
\stemDown a''8 [\stemDown f'''8] \stemDown c'''8 [\stemDown a''8]
\stemDown <a' a''>8 [\stemDown <c'' a''>8] <a' a''>4
\stemDown c'''16 [\stemDown f'''16 \stemDown e'''16 \stemDown f'''16] \stemDown g'''16 [\stemDown f'''16 \stemDown e'''16 \stemDown d'''16]
\stemDown e''8 [\stemDown c''8] \stemDown c'''8 [\stemDown g''8]
\stemDown cis''16 [\stemDown d''16 \stemDown f''16 \stemDown a''16] \stemDown g''8 [\stemDown b'8]
\stemDown a''8 [\stemDown f''8] \stemDown d''8 [\stemDown b'8]
\tuplet 3/2 {\grace { \stemUp b'8*3/2 } \stemDown c''8 [\stemDown e''8 \stemDown f''8]} f''4
\stemUp g'8 [\stemUp a'16 \stemUp g'16] \stemDown f''8 [\stemDown d''8]
\grace { \stemUp dis''8 } e''4 \grace { \stemUp dis''8 } \stemDown e''8 [\stemDown cis''8]
\stemDown a''8 [\stemDown f'''8] \stemDown c'''8 [\stemDown a''8]
\stemUp gis'8 [\stemUp b'8] \stemDown e''8 [\stemDown gis''8]
R2
\stemDown g''8 [\stemDown fis''16 \stemDown g''16] \stemDown a''16 [\stemDown g''16 \stemDown f''16 \stemDown d''16]
\stemUp e''8 [\stemUp e'8] e'4
\stemUp d''8 [\stemUp bes''16 \stemUp d'''16] \stemUp c'''8 [\stemUp e''8]
\stemDown a''16 [\stemDown bes''16 \stemDown c'''16 \stemDown d'''16] \stemDown bes''8 [\stemDown g''8]
\stemDown b''8 [\stemDown a''8] g''4
\stemDown bes''8 [\stemDown c'''16 \stemDown bes''16] \stemDown a''8 [\stemDown f''8]
\stemDown b''16 [\stemDown a''16 \stemDown gis''16 \stemDown fis''16] \stemDown e''8 [\stemDown b''8]
\grace { \stemUp b''8 } \stemDown c'''8 [\stemDown b''16 \stemDown a''16] \stemDown c'''8 [\stemDown b''16 \stemDown a''16]
\stemUp a''8 [\stemUp g''8] \stemUp f''8 [\stemUp d''8]
\stemDown e''16 [\stemDown dis''16 \stemDown e''16 \stemDown gis''16] \stemDown b''8 [\stemDown e''8]
\stemDown d'''8 [\stemDown e'''16 \stemDown f'''16] \stemDown f'''8 [\stemDown g''8]
\stemDown e'''8. [\stemDown d'''16] \stemDown b''8 [\stemDown c'''8]
\stemDown d''8 [\stemDown c'''8] \stemDown b''8 [\stemDown d''8]
\stemDown a''8 [\stemDown <c'' a''>8] <c'' a''>4
\stemDown f''16 [\stemDown g''16 \stemDown a''16 \stemDown f''16] \stemDown d''8 [\stemDown b'8]
\stemDown d'''16 [\stemDown c'''16 \stemDown b''16 \stemDown a''16] \stemDown b''8 [\stemDown g''8]
\stemDown c'''16 [\stemDown e'''16 \stemDown f'''16 \stemDown g'''16] \stemDown a'''8 [\stemDown a'''8]
\stemDown b''8 [\stemDown d'''16 \stemDown f'''16] \stemDown e'''8 [\stemDown gis''8]
\stemDown a''8 [\stemDown c'''16 \stemDown b''16] a''4
\stemDown e''16 [\stemDown e'''16 \stemDown c'''16 \stemDown a''16] \stemDown gis''16 [\stemDown e''16 \stemDown b''16 \stemDown gis''16]
\tuplet 3/2 {\stemDown e''8 [\stemDown g''8 \stemDown c''8] } a''4
\stemDown g''16 [\stemDown a''16 \stemDown bes''16 \stemDown c'''16] \stemDown a''8 [\stemDown f''8]
\stemDown a''8 [\stemDown a'''8] a''4
\stemDown cis'''16 [\stemDown d'''16 \stemDown e'''16 \stemDown f'''16] \stemDown c'''8 [\stemDown e''8]
\stemDown c''8 [\stemDown b''8] \stemDown a''8 [\stemDown c''8]
\stemDown c'''8 [\stemDown d'''16 \stemDown c'''16] \stemDown b''8 [\stemDown e''8]
\stemDown a''8 [\stemDown gis''16 \stemDown a''16] \stemDown b''8 [\stemDown e''8]
\stemDown d'''8 [\stemDown c'''8] \stemDown a''8 [\stemDown a''8]
\stemDown g''8 [\grace { \stemUp b''8 } \stemDown c'''8] \stemDown c'''8 [\stemDown c''8]
f'''4 \stemDown d'''8 [\stemDown a''8]
\stemDown c'''8 [\stemDown a'16 \stemDown b'16] \stemDown c''16 [\stemDown c''16 \stemDown c''16 \stemDown d''16]
\stemDown a''8. [\stemDown g''16] \stemDown e''8 [\stemDown f''8]
\stemDown a''16 [\stemDown b''16 \stemDown c'''16 \stemDown d'''16] \stemDown e'''8 [\stemDown a''8]
\stemDown a''16 [\stemDown g''16 \stemDown fis''16 \stemDown g''16] \stemDown a''8 [\stemDown b''8]
\stemDown g''8 [\stemDown fis''16 \stemDown g''16] \stemDown c'''8 [\stemDown e''8]
\stemDown a''8 [\stemDown f'''8] \stemDown c'''8 [\stemDown a''8]
c'''4 r4
\stemDown gis''8 [\stemDown e'''8] \stemDown c'''8 [\stemDown a''8]
\stemDown e'''8 [\stemDown d'''8] c'''4
\stemUp c'''8. [\stemUp bes''16] \stemUp a''8 [\stemUp a''8]
\stemDown f''16 [\stemDown e''16 \stemDown e''16 \stemDown c'''16] \stemDown c'''8 [\stemDown e''8]
\stemDown <a' f''>8 [\stemDown <c'' a''>8] <a' f''>4
\stemDown g''16 [\stemDown fis''16 \stemDown g''16 \stemDown d'''16] \stemDown c'''16 [\stemDown bes''16 \stemDown g''16 \stemDown e''16]
\stemDown cis''8 [\stemDown a''8] a'4
\stemDown c'''8 [\stemDown b''16 \stemDown c'''16] \stemDown e'''16 [\stemDown d'''16 \stemDown bes''16 \stemDown g''16] |
\stemDown bes''16 [\stemDown a''16 \stemDown gis''16 \stemDown a''16] f''4
\grace { \stemUp b'8 } c''4 \grace { \stemUp b'8 } c''4
\stemDown c'''8 [\stemDown b''8] a''4
\stemDown c''16 [\stemDown d''16 \stemDown e''16 \stemDown f''16] \stemDown g''8 [\stemDown bes''8]
\stemDown c''8 [\stemDown b'8] a'4
\stemDown bes''8 [\stemDown c'''16 \stemDown d'''16] \stemDown c'''8 [\stemDown f''8]
\tuplet 3/2 {\stemDown d''8 [\stemDown f''8 \stemDown a''8] } a''4
\grace { \stemUp c''8 } \stemDown e''8 [\grace { \stemUp e''8 } \stemDown g''8] \grace { \stemUp g''8 } \stemDown bes''8 [\grace {\stemUp bes''8 } \stemDown d'''8]
\stemDown c''8 [\stemDown e''8] c'''4
\tuplet 3/2 {\stemDown a''8 [\stemDown gis''8 \stemDown g''8] } \stemDown g''8 [\stemDown f''8]
\stemDown a''8 [\stemDown c'''8] a''4
\stemDown g''16 [\stemDown f''16 \stemDown e''16 \stemDown g''16] f''4
\stemDown f''8 [\stemDown <c'' a''>8] <a' f''>4"""

piano_right_hand_voice_2 = r"""s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
c''2
s2
s2
s2
s2
s2
s2
s2
s2
| c''2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
d''4 \stemDown c''8 [\stemDown b'8]
f'4 f'4
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
f'4 r4
s2
s2
s2
s2
s2
s2
s2
s2
s2
\stemDown g'8 [\stemDown f'8] e'4
s2
s2
s2
c''2
s2
s2
s2
s2
s2
s2
s2
s2
s2
a'2
b'2
s2
s2
s2
s2
s2
cis''4 d''4
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
r8 <d' g'>8 r8 <g' bes'>8
s2
s2
s2
s2
s2
b'2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
c''4 \stemDown c''8 [\stemDown c''8]
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2
s2"""

piano_left_hand_voice_1 = r"""r8 <b f'>8 \stemUp <d' f'>8 [\stemUp <b f'>8]
\stemDown a8 [\stemDown <c' e'>8] \stemDown d8 [\stemDown <a d'>8]
\stemDown <g d'>8 [\stemDown <a d'>8] <g d'>4
\stemDown e8 [\stemDown g8] \stemDown c'8 [\stemDown e'8]
\clef "treble" r8 <b e'>8 \stemUp <d' e'>8 [\stemUp <d' e'>8]
\clef "bass" r8 <e' g'>8 \stemUp <cis' g'>8 [\stemUp <cis' g'>8]
\stemDown <c' e'>8 [\stemDown c'8] c4
\stemDown a,8 [\stemDown <a c'>8] \stemDown <a c'>8 [\stemDown <a c'>8]
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
\stemDown <g b d'>8 [\stemDown <g b>8] <g b>4
\stemDown f8 [\stemDown <a d'>8] \stemDown g8 [\stemDown <d' f'>8]
\stemDown c8 [\stemDown e'8] c'4
<f f'>4 \stemDown <a e'>8 [\stemDown es'8]
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
r8 c'8 \stemUp c'8 [\stemUp c'8]
\clef "treble" r8 <f' g'>8 \stemUp <f' g'>8 [\stemUp <f' g'>8]
\clef "bass" \stemDown <e gis b>8 [\grace { \stemUp dis'8 } \stemDown e'8] e4
r8 <d' f'>8 \stemUp <d' f'>8 [\stemUp <d' f'>8]
<fis c' d'>4 \stemDown <g b d'>8 [\stemDown <gis b d'>8] |
r8 <a c'>8 \stemUp <a c'>8 [\stemUp <fis d'>8]
r8 <b f'>8 r8 <b f'>8
<fis a c' es'>4 <g c' e'>4
\stemDown g8 [\stemDown <d' e'>8] \stemDown b8 [\stemDown <d' e'>8]
\stemDown g8 [\stemDown <c' e'>8] \stemDown bes8 [\stemDown <c' g'>8]
r8 <bes c'>8 \stemUp <bes c'>8 [\stemUp <bes c'>8]
\stemDown a8 [\stemDown c'8] \stemDown e'8 [\stemDown a'8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
\stemDown <g c' e'>8 [\stemDown <g b f'>8] <c' e'>4
r8 <a d'>8 r8 <a d'>8
\stemDown c8 [\stemDown e8] \stemDown <c' e'>8 [\stemDown g8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown a8 [\stemDown <c' e'>8]
g2
\stemDown e8 [\stemDown <g b>8] \stemDown b,8 [\stemDown <fis b>8]
\stemDown <a c'>8 [\stemDown <a e'>8] <a c'>4
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
<f a d'>4 <fis a d'>4
\stemDown f8 [\stemDown <a d'>8] \stemDown <g c' e'>8 [\stemDown <g b f'>8]
r8 <a c'>8 \stemUp <a c'>8 [\stemUp <a c'>8]
\stemDown c8 [\stemDown g8] \stemDown <c' e'>8 [\stemDown g8] |
r8 c'8 \stemUp c'8 [\stemUp c'8]
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
r8 <cis' e'>8 \stemUp <cis' g'>8 [\stemUp <cis' g'>8]
r8 <c' f'>8 \stemUp <c' f'>8 [\stemUp <c' f'>8]
r8 <fis c'>8 r8 b8
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\stemDown e8 [\stemDown e'8] \stemDown <dis' e'>8 [\stemDown <d' e'>8]
r8 <b f'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
\stemDown <c' e'>8 [\stemDown g8] c4
\stemDown <c' e'>8 [\stemDown c'8] c4
\stemDown <c' e'>8 [\stemDown <e' g'>8] <c' e'>4
\stemDown <f a>8 [\stemDown c'8] <f a>4
r8 f'8 \stemUp e'8 [\stemUp d'8]
r8 b8 \stemUp b8 [\stemUp b8]
r8 <cis' g'>8 \stemUp <cis' g'>8 [\stemUp <cis' g'>8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
<g b f'>4 <g c' e'>4
\stemDown <g c' e'>8 [\stemDown <g b f'>8] <c' e'>4 |
\stemDown f8 [\stemDown a8] \stemDown d'8 [\stemDown f'8]
r8 <f b>8 \stemUp <f b>8 [\stemUp <f b>8]
<bes d' g'>4 <bes d' f'>4
\stemDown a8 [\stemDown <c' f'>8] \stemDown f8 [\stemDown <c' f'>8]
\stemUp <a, c>8 [\stemUp e,8] a,,4
r8 <g c'>8 \stemUp <g c'>8 [\stemUp <g c'>8]
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b d'>8]
<g bes c'>4 <f a c'>4
r8 f'8 r8 f'8
r8 <bes e'>8 r8 <a c'>8
\stemDown <g b>8 [\stemDown g8] g,4
r8 <a d'>8 \stemUp <a d'>8 [\stemUp <a d'>8]
\stemDown f8 [\stemDown <a d'>8] \stemDown <g c' e'>8 [\stemDown <g b f'>8]
\stemDown e8 [\stemDown <c' e'>8] \stemDown e8 [\stemDown <b d'>8]
r8 <c' e'>8 r8 <c' e'>8
r8 <c' d'>8 \stemUp <c' d'>8 [\stemUp <c' d'>8]
\stemDown a8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\stemDown c8 [\stemDown c'8] \stemDown <b c'>8 [\stemDown <bes c'>8]
\stemDown fis8 [\stemDown <a d'>8] \stemDown fis8 [\stemDown <c' d'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
\stemDown d8 [\stemDown <d' f'>8] \stemDown <d' f'>8 [\stemDown <d' f'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
\stemDown e8 [\stemDown <gis d'>8] \stemDown gis8 [\stemDown <d' e'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
\stemDown bes,8 [\stemDown <bes d'>8] \stemDown <bes d'>8 [\stemDown <bes d'>8]
\stemDown <a c'>8 [\stemDown <fis a d'>8] \stemDown <g b f'>8 [\stemDown <a c' e'>8]
r8 c'8 \stemUp c'8 [\stemUp c'8]
\stemDown a,8 [\stemDown <a c'>8] \stemDown <a c'>8 [\stemDown <a c'>8]
r8 c'8 \stemUp c'8 [\stemUp c'8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\stemDown <g d' f'>8 [\stemDown <g d' f'>8] <c' e'>4
r8 <c' d'>8 r8 <c' d'>8
<e gis b>4 \stemDown e'8 [\stemDown e8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\stemDown <g c'>8 [\stemDown <g b>8] <c c'>4
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' g'>8]
r8 <c' f'>8 \stemUp <c' f'>8 [\stemUp <c' f'>8]
r8 c'8 c'4
\stemDown <c' e'>8. [\stemDown b16] \stemDown a8 [\stemDown <c' e'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
e4 \stemDown f8 [\stemDown f8]
\stemDown <c' e'>8 [\stemDown g8] c4
r8 <a b d'>8 \stemUp <e c'>8 [\stemUp <e b d'>8]
r8 <a d'>8 \stemUp <e a e'>8 [\stemUp <e gis d'>8]
r8 <fis c'>8 \stemUp <fis c'>8 [\stemUp <fis c'>8]
<e b d'>4 <e a c'>4
r8 <b f'>8 \stemUp <b f'>8 [\stemUp <b f'>8]
r8 <c' f'>8 \stemUp <c' f'>8 [\stemUp <c' f'>8]
\stemUp a8. [\stemUp g16] f4
\stemUp g,8 [\stemUp g8] \stemDown <d' f'>8 [\stemDown b8]
\stemDown gis8 [\stemDown <b e'>8] \stemDown a8 [\stemDown <c' e'>8]
r8 <gis d'>8 \stemUp <gis d'>8 [\stemUp <gis d'>8]
\stemDown a,8 [\stemDown <c' e'>8] \stemDown a8 [\stemDown <c' e'>8]
\stemDown d8 [\stemDown <a b>8] \stemDown e8 [\stemDown <b d'>8]
\stemDown c8 [\stemDown <g e'>8] \stemDown <g e'>8 [\stemDown <bes e'>8]
r8 e'8 d'8 r8
\stemDown g8 [\stemDown <b f'>8] \stemDown g8 [\stemDown <b f'>8]
r8 <b e'>8 \stemUp <b e'>8 [\stemUp <b e'>8]
r8 <a e'>8 \stemUp <a e'>8 [\stemUp <a e'>8]
\stemDown <a c'>8 [\stemDown e8] a,4
<d' f'>4 \stemDown <c' d'>8 [\stemDown <b d'>8]
\stemDown d8 [\stemDown f'8] d'4
r8 <c' f'>8 \stemUp <c' f'>8 [\stemUp <c' f'>8]
\stemDown <a c'>8 [\stemDown e8] a,4
r8 <c' f'>8 r8 <d' f'>8
r8 <bes e'>8 \stemUp <bes e'>8 [\stemUp <bes e'>8]
r8 <a d'>8 r8 <d' f'>8
<f c' d'>4 \stemDown <g b d'>8 [\stemDown <g d' f'>8]
r8 <a f'>8 \stemUp <a f'>8 [\stemUp <a f'>8]
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <b f'>8]
r8 <cis' g'>8 \stemUp <cis' g'>8 [\stemUp <e' g'>8]
r8 <c' f'>8 \stemUp <c' f'>8 [\stemUp <c' f'>8]
r8 <gis d'>8 \stemUp <b e'>8 [\stemUp <b e'>8]
a4 \stemUp c'8 [\stemUp e'8]
r8 <b d'>8 \stemUp <b f'>8 [\stemUp <b f'>8]
\stemDown <e g b>8 [\stemDown <e g c'>8] <e g>4
bes4 c'4
r8 <a d'>8 r8 <bes d'>8
\stemDown <g b d'>8 [\stemDown <fis c' d'>8] <g b f'>4 |
r8 <c' e'>8 r8 <a c'>8
r8 <gis d'>8 \stemUp <gis d'>8 [\stemUp <gis d'>8]
r8 <c' es'>8 r8 <c' es'>8
\stemUp g,8 [\stemUp g8] \stemDown <d' f'>8 [\stemDown g8]
r8 <b e'>8 r8 <d' e'>8
<gis b f'>4 <g b f'>4
r8 <b e'>8 \stemUp <b e'>8 [\stemUp <b e'>8]
\stemDown d8 [\stemDown <a f'>8] \stemDown e8 [\stemDown <b e'>8]
\stemDown <a c'>8 [\stemDown <a e'>8] <a c'>4
r8 <b d'>8 \stemUp <b d'>8 [\stemUp <d' f'>8]
r8 <c' d'>8 r8 <b d'>8
r8 <c' f'>8 r8 <c' f'>8
r8 <a b>8 r8 <b d'>8
\stemDown <a c'>8 [\stemDown <e gis d'>8] <a c'>4
\stemDown e8 [\stemDown <c' e'>8] \stemDown <e b d'>8 [\stemDown <e b d'>8]
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
r8 <g c'>8 r8 <a c'>8
\stemDown <a c'>8 [\stemDown e8] a,4
\clef "treble" \stemUp <bes d' g'>8 [\stemUp <b d' gis'>8] \stemUp <c' f' a'>8 [\stemUp <c' g' bes'>8]
\clef "bass" \stemDown e8 [\stemDown <c' e'>8] \stemDown f8 [\stemDown <a f'>8]
r8 <c' e'>8 r8 <d' e'>8
r8 <b d'>8 r8 <gis d' e'>8
\stemDown a8 [\stemDown <c' e'>8] \stemDown f8 [\stemDown <c' d'>8]
\stemDown <c e g>8 [\stemDown c'8] \stemDown c'8 [\stemDown c8]
\stemDown d8 [\stemDown <d' f'>8] \stemDown <d' f'>8 [\stemDown <d' f'>8]
\stemDown <a, a>8 [\stemDown <c' e'>8] \stemDown a8 [\stemDown <c' e'>8]
r8 <cis' g'>8 \stemUp <cis' g'>8 [\stemUp <cis' g'>8]
r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
r8 <b f'>8 \stemUp <d' f'>8 [\stemUp <d' f'>8]
<g b f'>4 \stemDown <g c' e'>8 [\stemDown <g bes c'>8] |
\stemDown f8 [\stemDown <a f'>8] \stemDown a8 [\stemDown <c' f'>8]
\stemDown <c' e'>8 [\stemDown g'8] <c' e'>4
r8 <gis e'>8 r8 <c' e'>8
\stemUp g8 [\stemUp f8] e4
r8 <c' e'>8 r8 <c' f'>8
r8 <c' e'>8 r8 <c' e'>8
\stemDown a'8 [\stemDown f'8] f4
\clef "treble" r8 <d' g'>8 r8 <g' bes'>8
<a a'>4 a4
\clef "bass" r8 <c' e'>8 \stemUp <c' e'>8 [\stemUp <c' e'>8]
r8 <c' f'>8 r8 <c' f'>8
r8 <a f'>8 \stemUp <a f'>8 [\stemUp <a f'>8]
\stemUp <c' e'>8 [\stemUp d'8] c'4
r8 <c' e'>8 r8 <c' e'>8
\stemUp e'8 [\stemUp d'8] c'4
<g c' e'>4 <a c' f'>4
\stemDown d8 [\stemDown <d' f'>8] \stemDown <d' f'>8 [\stemDown <d' f'>8]
r8 <c' e'>8 r8 <c' e'>8
\stemDown c8 [\stemDown <c' e'>8] \stemDown <c' e'>8 [\stemDown <c' e'>8]
\clef "treble" r8 <d' f' g'>8 \stemUp <d' f' g'>8 [\stemUp <d' f' g'>8]
\clef "bass" \stemDown <a c'>8 [\stemDown <a e'>8] <a c'>4
\stemDown d8 [\stemDown <a f'>8] \stemDown <a f'>8 [\stemDown <a f'>8]
\stemUp <f, a,>8 [\stemUp c,8] a,,4"""

piano_left_hand_voice_2 = r"""g2
s2
s2
s2
gis2
a2
s2
s2
g2
s2
s2
s2
s2
g2
c2
b2
s2
d4 s4
s2
d2
g4 g4
s2
s2
s2
c2
s2
a2
s2
f4 d4
s2
s2
s2
s2
s2
a2
s2
s2
f2
s2
c2
e2
a4 s4
f2
d4 g4
g2
s2
s2
s2
g2
s2
s2
s2
s2
f4 \stemDown e8 [\stemDown e8]
g2
a2
s2
s2
s2
s2
d2
s2
s2
s2
c2
g2
s2
c'4 d'4
c4 f4
s2
fis2
s2
s2
a4 a4
fis2
s2
s2
s2
a2
s2
g2
s2
a2
a2
s2
s2
c2
s2
c2
s2
s2
a4 fis4
s2
s2
s2
s2
a2
c2
s2
c2
s2
s2
f4 s4
f4 s4
d2
s2
g2
f2
c'2
s2
s2
e2
s2
s2
s2
a4 r8 d8
s2
gis2
e2
s2
s2
s2
f2
s2
a4 bes4
g2
f4 g4
s2
f2
g2
a2
f2
e2
a,4 \stemDown c8 [\stemDown e8]
g2
s2
s2
fis4 g4
s2
g4 f4
e2
fis4 f4
s2
gis4 gis4
s2
gis2
s2
s2
g2
fis4 g4
a4 f4
d4 e4
s2
s2
s2
e4 f4
s2
s2
s2
a4 gis4
f4 e4
s2
s2
s2
s2
a2
a2
g2
s2
s2
s2
e4 a4
c2
g4 f4
g4 a4
s2
bes4 c'4
s2
g2
f4 a4
f2
a2
bes4 g4
a2
s2
s2
bes4 g4
s2
b2
s2
s2
s2"""

rh_v_1 = piano_right_hand_voice_1.split('\n')
rh_v_2 = piano_right_hand_voice_2.split('\n')

lh_v_1 = piano_left_hand_voice_1.split('\n')
lh_v_2 = piano_left_hand_voice_2.split('\n')

voice_format = r'{{<<{{\voiceOne {voice_1}}} \new Voice {{\voiceTwo {voice_2}}}>>}}'


piano_right_hand = []
for rhv1, rhv2 in zip(rh_v_1, rh_v_2):
    if rhv2.startswith('s2'):
        piano_right_hand.append(rhv1.strip())
    else:
        piano_right_hand.append(voice_format.format(voice_1=rhv1.strip(), voice_2=rhv2.strip()))


piano_left_hand = []
for lhv1, lhv2 in zip(lh_v_1, lh_v_2):
    if lhv2.startswith('s2'):
        piano_left_hand.append(lhv1.strip())
    else:
        piano_left_hand.append(voice_format.format(voice_1=lhv1.strip(), voice_2=lhv2.strip()))


sync_bars = {}
for ind, (piano_right_hand, piano_left_hand) in enumerate(zip(piano_right_hand, piano_left_hand)):
    sync_bars[ind + 1] = {'piano_right_hand': SimpleBar(piano_right_hand),
                          'piano_left_hand': SimpleBar(piano_left_hand)}

a = SimpleBarCollection(sync_bars)

writer = SimpleBarCollectionCSVWriter()
writer.write_csv(a, Path('/tmp/scottish_dance_bars.csv'))

print()
