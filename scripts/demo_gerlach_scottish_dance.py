__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.dice_games import GerlachScottishDance
from musical_games.utils import auto_convert_lilypond_file

out_dir = Path('/tmp/test')

dice_game = GerlachScottishDance()

dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
auto_convert_lilypond_file(out_dir / 'overview.ly')

dice_game.compile_single_bar('dance', 6).to_file(out_dir / 'bar_dance_6.ly')
auto_convert_lilypond_file(out_dir / 'bar_dance_6.ly')
dice_game.compile_single_bar('trio', 158).to_file(out_dir / 'bar_trio_158.ly')
auto_convert_lilypond_file(out_dir / 'bar_trio_158.ly')

dice_game.compile_single_dice_table_element('dance',
                                            dice_game.get_dice_tables()['dance'].get_elements()[0]).to_file(
    out_dir / 'single_dice_table_element_dance_0.ly')
auto_convert_lilypond_file(out_dir / 'single_dice_table_element_dance_0.ly')

dice_game.compile_single_dice_table_element('trio',
                                            dice_game.get_dice_tables()['trio'].get_element(3, 7)).to_file(
    out_dir / 'single_dice_table_element_trio_3_7.ly')
auto_convert_lilypond_file(out_dir / 'single_dice_table_element_trio_3_7.ly')

print(dice_game.get_duplicate_dice_table_elements('dance'))
print(dice_game.get_duplicate_dice_table_elements('trio'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

bar_selection = dice_game.get_random_bar_selection(seed=10)

dice_game.compile_composition_score(bar_selection,
                                    comment='Test', single_page=True).to_file(out_dir / 'composition_pdf.ly')
auto_convert_lilypond_file(out_dir / 'composition_pdf.ly')

midi_settings = dice_game.get_default_midi_settings()
my_midi_settings = midi_settings.with_updated_instrument('flute', 'dance', 'piano_right_hand')

dice_game.compile_composition_audio(bar_selection,
                                    midi_settings=my_midi_settings).to_file(out_dir / 'composition_midi.ly')

auto_convert_lilypond_file(
    out_dir / 'composition_midi.ly',
    soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))
