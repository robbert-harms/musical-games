from musical_games.dice_games.compositions import MozartWaltzInfo, KirnbergerMenuetTrioInfo, StadlerMenuetTrio, \
    StadlerMenuetTrioInfo
from musical_games.dice_games.lilypond.base import MusicBookComment
from musical_games.utils import write_lilypond_file, auto_convert_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


soundfont = '/home/robbert/programming/www/opus-infinity.org/soundfonts/steinway_grand_piano.sf2'

composition_info = MozartWaltzInfo()
composition = composition_info.get_composition('piano')

# dice_tables = composition.get_dice_tables()
# indices = {table.name: [54, 95, 27, 63, 161, 46, 159, 24, 102, 20, 7, 82, 144, 49, 1, 79] for table in dice_tables}
# lilypond = composition.typeset_composition(indices, comments=MusicBookComment('', '', 'Test'))
# write_lilypond_file('/tmp/musical_games/mozart.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/mozart.ly', soundfont)

# dice_table = composition.get_dice_tables()[0]
# lilypond = composition.typeset_single_measure(dice_table.name, dice_table.random_index(0))
# write_lilypond_file('/tmp/musical_games/mozart_single_measure.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/mozart_single_measure.ly', pdf=False)


# lilypond = composition.typeset_measure_overview()
# write_lilypond_file('/tmp/musical_games/mozart.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/mozart.ly')


composition_info = KirnbergerMenuetTrioInfo()
composition = composition_info.get_composition('piano')

# dice_tables = composition.get_dice_tables()
# indices = {table.name: table.random_indices() for table in dice_tables}
# lilypond = composition.typeset_composition(indices, comments=MusicBookComment('', '', 'Test'))
# write_lilypond_file('/tmp/musical_games/kb.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/kb.ly', soundfont)

# dice_table = composition.get_dice_tables()[0]
# lilypond = composition.typeset_single_measure(dice_table.name, dice_table.random_index(0))
# write_lilypond_file('/tmp/musical_games/kb_single_measure.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/kb_single_measure.ly')

lilypond = composition.typeset_measure_overview()
write_lilypond_file('/tmp/musical_games/kbmt.ly', lilypond)
auto_convert_lilypond_file('/tmp/musical_games/kbmt.ly')


composition_info = StadlerMenuetTrioInfo()
composition = composition_info.get_composition('piano')

# dice_tables = composition.get_dice_tables()
# indices = {table.name: table.random_indices() for table in dice_tables}
# lilypond = composition.typeset_composition(indices, comments=MusicBookComment('', '', 'Test'))
# write_lilypond_file('/tmp/musical_games/std.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/std.ly', soundfont)

# dice_table = composition.get_dice_tables()[0]
# lilypond = composition.typeset_single_measure(dice_table.name, dice_table.random_index(0))
# write_lilypond_file('/tmp/musical_games/stadler_single_measure.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/stadler_single_measure.ly')

# lilypond = composition.typeset_measure_overview()
# write_lilypond_file('/tmp/musical_games/stadler.ly', lilypond)
# auto_convert_lilypond_file('/tmp/musical_games/stadler.ly')