__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from musical_games.dice_games import load_inbuilt_dice_game
from musical_games.utils import auto_convert_lilypond_file

dice_game = load_inbuilt_dice_game('cpe_bach_counterpoint')

dice_game.typeset_bars_overview('/tmp/test/overview.ly', render_options={'large_page': True})
auto_convert_lilypond_file('/tmp/test/overview.ly')

dice_game.typeset_single_bar('treble', 1, '/tmp/test/bar_treble_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_treble_1.ly')
dice_game.typeset_single_bar('bass', 1, '/tmp/test/bar_bass_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_bass_1.ly')

print(dice_game.get_duplicate_bars('bass'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

composition = dice_game.random_composition()
composition.typeset('/tmp/test/composition.ly')
auto_convert_lilypond_file('/tmp/test/composition.ly',
                           sound_font='/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2')
