from musical_games.utils import auto_convert_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


lilypond_file = '/tmp/test/tester.ly'
soundfont = '/home/robbert/programming/www/opus-infinity.org/soundfonts/steinway_grand_piano.sf2'
auto_convert_lilypond_file(lilypond_file, soundfont)