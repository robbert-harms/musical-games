__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.dice_games import MozartWaltz
from musical_games.utils import auto_convert_lilypond_file

out_dir = Path('/tmp/test')

dice_game = MozartWaltz()

dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
auto_convert_lilypond_file(out_dir / 'overview.ly')

dice_game.compile_single_bar('waltz', 5).to_file(out_dir / 'bar_waltz_1.ly')
auto_convert_lilypond_file(out_dir / 'bar_waltz_1.ly')

dice_game.compile_single_dice_table_element('waltz',
                                            dice_game.get_dice_tables()['waltz'].get_elements()[0]).to_file(
    out_dir / 'single_dice_table_element_waltz_0.ly')
auto_convert_lilypond_file(out_dir / 'single_dice_table_element_waltz_0.ly')

print(dice_game.get_duplicate_dice_table_elements('waltz'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

dice_game.compile_composition_score(dice_game.get_random_bar_selection(seed=1, shuffle_staffs=False),
                                    comment='Test', single_page=True).to_file(out_dir / 'composition_pdf.ly')
auto_convert_lilypond_file(out_dir / 'composition_pdf.ly')

midi_settings = dice_game.get_default_midi_settings()
my_midi_settings = midi_settings.with_updated_instrument('flute', 'waltz', 'piano_right_hand')

dice_game.compile_composition_audio(
    dice_game.get_random_bar_selection(seed=0),
    midi_settings=my_midi_settings).to_file(out_dir / 'composition_midi.ly')

auto_convert_lilypond_file(
    out_dir / 'composition_midi.ly',
    soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))

