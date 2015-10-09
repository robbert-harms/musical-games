from musical_games.dice_games.compositions import MozartWaltzInfo, KirnbergerMenuetTrioInfo
from musical_games.utils import write_lilypond_file, auto_convert_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


# composition_info = MozartWaltzInfo()
# composition = composition_info.get_composition('piano')
# lilypond = composition.typeset_measure_overview()
#
# write_lilypond_file('/tmp/musical_games/mozart.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/mozart.ly')


composition_info = KirnbergerMenuetTrioInfo()
composition = composition_info.get_composition('piano')
lilypond = composition.typeset_measure_overview()

write_lilypond_file('/tmp/musical_games/kbmt.ly', lilypond)
auto_convert_lilypond_file('/tmp/musical_games/kbmt.ly')