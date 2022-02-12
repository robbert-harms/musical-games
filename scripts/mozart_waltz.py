__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from musical_games.dice_games.dice_games import MozartWaltz
from musical_games.dice_games.typesetting import MidiSettings
from musical_games.utils import auto_convert_lilypond_file

dice_game = MozartWaltz()

dice_game.typeset_bars_overview(render_settings={'large_page': True}, out_file='/tmp/test/overview.ly')
auto_convert_lilypond_file('/tmp/test/overview.ly')

dice_game.typeset_single_bar('waltz', 5, out_file='/tmp/test/bar_waltz_1.ly')
auto_convert_lilypond_file('/tmp/test/bar_waltz_1.ly')

print(dice_game.game_mechanics.get_all_duplicate_bars('waltz'))
print(dice_game.game_mechanics.count_unique_compositions(count_duplicates=True))
print(dice_game.game_mechanics.count_unique_compositions(count_duplicates=False))

dice_game.typeset_composition_pdf(
    dice_game.game_mechanics.get_random_bar_nmrs(seed=0),
    render_settings={'comment': 'Test'},
    out_file='/tmp/test/composition_pdf.ly')
auto_convert_lilypond_file('/tmp/test/composition_pdf.ly')

dice_game.typeset_composition_midi(
    dice_game.game_mechanics.get_random_bar_nmrs(seed=0),
    render_settings={'piano_rh_midi_settings': MidiSettings('violin', 0, 1)},
    out_file='/tmp/test/composition_midi.ly')

auto_convert_lilypond_file('/tmp/test/composition_midi.ly',
                           sound_font='/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2')
