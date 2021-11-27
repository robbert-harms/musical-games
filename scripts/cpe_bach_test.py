__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from musical_games.dice_games import load_inbuilt_dice_game, load_inbuilt_dice_game_typesetter
from musical_games.utils import auto_convert_lilypond_file

dice_game = load_inbuilt_dice_game('cpe_bach_counterpoint')
dice_game_typesetter = load_inbuilt_dice_game_typesetter(dice_game, 'cpe_bach_counterpoint')

dice_game_typesetter.typeset_bars_overview({'large_page': True}, '/tmp/test/overview.ly')
auto_convert_lilypond_file('/tmp/test/overview.ly')

dice_game_typesetter.typeset_single_bar('treble', 1, '/tmp/test/bar_treble_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_treble_1.ly')
dice_game_typesetter.typeset_single_bar('bass', 1, '/tmp/test/bar_bass_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_bass_1.ly')

print(dice_game.get_duplicate_bars('bass'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

dice_game_typesetter.typeset_composition(dice_game.get_random_bar_nmrs(seed=0),
                                         out_file='/tmp/test/composition.ly')
auto_convert_lilypond_file('/tmp/test/composition.ly',
                           sound_font='/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2')
