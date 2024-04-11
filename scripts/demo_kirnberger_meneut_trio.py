__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games2.kirnberger_menuet_trio import KirnbergerMenuetTrio
from musical_games.utils import auto_convert_lilypond_file

out_dir = Path('/tmp/test2')

dice_game = KirnbergerMenuetTrio()

dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
auto_convert_lilypond_file(out_dir / 'overview.ly')


# dice_game.typeset_single_bar('menuet', 1, out_file='/tmp/test/bar_menuet_1.ly')
# auto_convert_lilypond_file(Path('/tmp/test/bar_menuet_1.ly'))
# dice_game.typeset_single_bar('trio', 1, out_file='/tmp/test/bar_trio_1.ly')
# auto_convert_lilypond_file(Path('/tmp/test/bar_trio_1.ly'))
#
# print(dice_game.game_mechanics.get_all_duplicate_bars('menuet'))
# print(dice_game.game_mechanics.count_unique_compositions(count_duplicates=True))
# print(dice_game.game_mechanics.count_unique_compositions(count_duplicates=False))
#
# dice_game.typeset_composition_pdf(
#     dice_game.game_mechanics.get_random_bar_nmrs(seed=0),
#     render_settings={'comment': 'Test'},
#     out_file='/tmp/test/composition_pdf.ly')
#
# auto_convert_lilypond_file(Path('/tmp/test/composition_pdf.ly'))
#
# dice_game.typeset_composition_midi(
#     dice_game.game_mechanics.get_random_bar_nmrs(seed=0),
#     render_settings={'menuet_bass_midi_settings': MidiSettings('flute', 0, 1)},
#     out_file='/tmp/test/composition_midi.ly')
#
# auto_convert_lilypond_file(
#     Path('/tmp/test/composition_midi.ly'),
#     soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))



# dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
# auto_convert_lilypond_file(out_dir / 'overview.ly')
#
# dice_game.compile_single_bar('treble', 1).to_file(out_dir / 'bar_treble_1.ly')
# auto_convert_lilypond_file(out_dir / 'bar_treble_1.ly')
# dice_game.compile_single_bar('bass', 1).to_file(out_dir / 'bar_bass_1.ly')
# auto_convert_lilypond_file(out_dir / 'bar_bass_1.ly')
#
# print(dice_game.get_all_duplicate_bars('bass'))
# print(dice_game.count_unique_compositions(count_duplicates=True))
# print(dice_game.count_unique_compositions(count_duplicates=False))
#
# dice_game.compile_composition_score(dice_game.get_random_bar_selection(seed=0),
#                                     comment='Test').to_file(out_dir / 'composition_pdf.ly')
# auto_convert_lilypond_file(out_dir / 'composition_pdf.ly')
#
# midi_settings = dice_game.get_default_midi_settings()
# my_midi_settings = midi_settings.with_updated_instrument('flute', 'treble', 0)
#
# dice_game.compile_composition_audio(
#     dice_game.get_random_bar_selection(seed=0),
#     midi_settings=my_midi_settings).to_file(out_dir / 'composition_midi.ly')
#
# auto_convert_lilypond_file(
#     out_dir / 'composition_midi.ly',
#     soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))
#
