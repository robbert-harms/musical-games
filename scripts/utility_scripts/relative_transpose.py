__author__ = 'Robbert Harms'
__date__ = '2024-06-06'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


from ly.document import Document
from ly.pitch.transpose import ModalTransposer, transpose
from ly.document import Cursor
from ly.music import document

txt = r'''{
\set Score.currentBarNumber = #3 g'4.( a'16) [ b'16 ] a'4 c''8. [ fis''16 ]
\set Score.currentBarNumber = #4 \partial 2. <fis' fis''>4 r4 r4
\set Score.currentBarNumber = #5 a'4. a'8 \grace { a'8 } g'8[ fis'8] g'8 a'8
\set Score.currentBarNumber = #6 c''4.( d''16) e''16 d''4 d''8.\noBeam b'16
\set Score.currentBarNumber = #7 \partial 2. b'4 r4 r4
\set Score.currentBarNumber = #8 c''4 fis''8. e''16 d''4 fis''16[ d''16] e''16 fis''16
\set Score.currentBarNumber = #9 c''8[ fis''8] eis''8[ d''8 ] c''8[ d''8] eis''8[ g''8 ]
\set Score.currentBarNumber = #10 e''4. c''8 d''4 fis''8.\noBeam d''16
\set Score.currentBarNumber = #11 c''4.\fermata d''8 c''4 fis''8.\noBeam fis''16
\set Score.currentBarNumber = #12 c''4. d''16 e''16 d''4 b''8. fis''16
\set Score.currentBarNumber = #13 c''4 c''16( [ d''16 e''16 c''16 ] ) b'4 fis''8.\noBeam fis''16
\set Score.currentBarNumber = #14 \partial 2. b'4 r4 r4
\set Score.currentBarNumber = #15 c''4. d''16 [ e''16 ] d''4 fis''8.\noBeam [ fis''16 ]
\set Score.currentBarNumber = #16 fis''4 \times 2/3 { d''8 [ b'8 g'8 ] } fis'4 \grace { a'16 } g'8.\noBeam [ fis'16 ]
\set Score.currentBarNumber = #17 e''4.( g''16) fis''16 e''4 c''8.\noBeam fis''16
\set Score.currentBarNumber = #18 b'8 [ a'8] b'8[ c''8 ] d''8[ b'8] d''8[ e''8 ]
\set Score.currentBarNumber = #0 \partial 4 fis''8.( fis''16)
\set Score.currentBarNumber = #19 a''4. fis''8 \grace{e''8} d''4 c''8 bis'8
\set Score.currentBarNumber = #20 g''8[ b''8] a''8[ g''8] fis''8[ e''8] d''8[ c''8]
\set Score.currentBarNumber = #21 g''4( g''16) fis''16 e''16 d''16 c''4 c''8.\noBeam fis''16
\set Score.currentBarNumber = #22 \partial 2. \grace{c''4} b'2 r4
\set Score.currentBarNumber = #23 b'4 d''8.( c''16) b'4 b'4
\set Score.currentBarNumber = #24 eis''8 [ fis''8] g''8[ fis''8 ] b''8 [ fis''8] d''8[ a'8 ]
\set Score.currentBarNumber = #0 \partial 4 fis''8. fis''16
\set Score.currentBarNumber = #25 e''4( c''8)\noBeam g''8 g''4( fis''8) e''8
\set Score.currentBarNumber = #26 fis''4. eis''8 e''8[ c''8] d''8 b'8]

}'''
lilypond_document = Document(txt)
cursor = Cursor(lilypond_document)

transposer = ModalTransposer(-2)

# m = ly.music.document(d)

transpose(cursor, transposer)

new_doc = document(lilypond_document)
# print(new_doc.dump())

print(lilypond_document.plaintext())

# print(ly.music.document(d))

# pitch_iterator = PitchIterator(d)
# for item in pitch_iterator.tokens():
#     print(item)

# for music in m.iter_music():
#     if isinstance(music, Note):
#         print(music)
#
#         transposer.transpose(music.pitch)
#         print(music)
#
#
#     # print(music)
#



