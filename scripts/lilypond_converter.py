from musical_games.utils import auto_convert_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


lilypond_file = '/tmp/test/composition.ly'
soundfont = '/home/robbert/programming/python/opus_infinity.org/soundfonts/Steinway_Grand_Piano_1.2.sf2'
auto_convert_lilypond_file(lilypond_file, soundfont)
