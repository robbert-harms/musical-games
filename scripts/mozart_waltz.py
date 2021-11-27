__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from musical_games.dice_games import load_inbuilt_dice_game, load_inbuilt_dice_game_typesetter
from musical_games.utils import auto_convert_lilypond_file

dice_game = load_inbuilt_dice_game('mozart_waltz')
dice_game_typesetter = load_inbuilt_dice_game_typesetter(dice_game, 'mozart_waltz')

dice_game_typesetter.typeset_bars_overview(render_options={'large_page': True}, out_file='/tmp/test/overview.ly')
auto_convert_lilypond_file('/tmp/test/overview.ly')

dice_game_typesetter.typeset_single_bar('waltz', 5, '/tmp/test/bar_waltz_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_waltz_1.ly')

print(dice_game.get_duplicate_bars('waltz'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

dice_game_typesetter.typeset_composition(dice_game.get_random_bar_nmrs(seed=0),
                                         render_options={'comment': 'Comment'},
                                         out_file='/tmp/test/composition.ly')
auto_convert_lilypond_file('/tmp/test/composition.ly',
                           sound_font='/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2')
