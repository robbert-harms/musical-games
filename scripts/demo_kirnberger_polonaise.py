__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.dice_games import KirnbergerPolonaise
from musical_games.utils import auto_convert_lilypond_file

out_dir = Path('/tmp/test2')

dice_game = KirnbergerPolonaise()

dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
auto_convert_lilypond_file(out_dir / 'overview.ly')

dice_game.compile_single_bar('polonaise', 1).to_file(out_dir / 'bar_polonaise_1.ly')
auto_convert_lilypond_file(out_dir / 'bar_polonaise_1.ly')

print(dice_game.get_all_duplicate_bars())
print(dice_game.get_duplicate_bars('polonaise', 88))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

print(dice_game.get_random_bar_selection(shuffle_staffs=False, seed=0))
print(dice_game.get_random_bar_selection(shuffle_staffs=True, seed=0))

dice_game.compile_composition_score(dice_game.get_random_bar_selection(shuffle_staffs=True, seed=0),
                                    comment='Test', single_page=True).to_file(out_dir / 'composition_pdf.ly')
auto_convert_lilypond_file(out_dir / 'composition_pdf.ly')

midi_settings = dice_game.get_default_midi_settings()
my_midi_settings = midi_settings.with_updated_instrument('flute', 'polonaise', 'violin_1')

dice_game.compile_composition_audio(
    dice_game.get_random_bar_selection(seed=0),
    midi_settings=my_midi_settings).to_file(out_dir / 'composition_midi.ly')

auto_convert_lilypond_file(
    out_dir / 'composition_midi.ly',
    soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))
