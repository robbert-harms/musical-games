from musical_games.dice_games.compositions import MozartWaltzInfo
from musical_games.utils import write_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


composition_info = MozartWaltzInfo()
composition = composition_info.get_composition('piano')
lilypond = composition.typeset_measure_overview()

write_lilypond_file('/tmp/test/test.ly', lilypond)


print(lilypond)