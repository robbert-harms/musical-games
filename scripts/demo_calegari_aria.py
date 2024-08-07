__author__ = 'Robbert Harms'
__date__ = '2021-03-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

from musical_games.dice_games.base import GroupedStaffsBarSelection
from musical_games.dice_games.dice_games import CalegariAria
from musical_games.utils import auto_convert_lilypond_file

out_dir = Path('/tmp/test')

dice_game = CalegariAria()

dice_game.compile_bars_overview(single_page=True).to_file(out_dir / 'overview.ly')
auto_convert_lilypond_file(out_dir / 'overview.ly')

dice_game.compile_single_bar('part_one', 1).to_file(out_dir / 'bar_1.ly')
auto_convert_lilypond_file(out_dir / 'bar_1.ly')
dice_game.compile_single_bar('part_one', 19).to_file(out_dir / 'bar_19.ly')
auto_convert_lilypond_file(out_dir / 'bar_19.ly')

dice_game.compile_single_dice_table_element('part_one', dice_game.get_dice_tables()['part_one'].get_elements()[0]).to_file(
    out_dir / 'single_dice_table_element_0.ly')
auto_convert_lilypond_file(out_dir / 'single_dice_table_element_0.ly')

print(dice_game.get_duplicate_dice_table_elements('part_one'))
print(dice_game.get_duplicate_dice_table_elements('part_two'))
print(dice_game.count_unique_compositions(count_duplicates=True))
print(dice_game.count_unique_compositions(count_duplicates=False))

dice_tables = dice_game.get_dice_tables()
selection = GroupedStaffsBarSelection(
    {'part_one': [dice_tables['part_one'].get_dice_throw(5, 0),
                  dice_tables['part_one'].get_dice_throw(8, 1),
                  dice_tables['part_one'].get_dice_throw(6, 2),
                  dice_tables['part_one'].get_dice_throw(3, 3),
                  dice_tables['part_one'].get_dice_throw(7, 4),
                  dice_tables['part_one'].get_dice_throw(4, 5),
                  dice_tables['part_one'].get_dice_throw(10, 6),
                  dice_tables['part_one'].get_dice_throw(9, 7)],
     'part_two': [dice_tables['part_two'].get_dice_throw(6, 0),
                  dice_tables['part_two'].get_dice_throw(10, 1),
                  dice_tables['part_two'].get_dice_throw(3, 2),
                  dice_tables['part_two'].get_dice_throw(5, 3),
                  dice_tables['part_two'].get_dice_throw(11, 4),
                  dice_tables['part_two'].get_dice_throw(4, 5),
                  dice_tables['part_two'].get_dice_throw(2, 6),
                  dice_tables['part_two'].get_dice_throw(3, 7),
                  dice_tables['part_two'].get_dice_throw(3, 8),
                  dice_tables['part_two'].get_dice_throw(11, 9)]}
)

for el in selection.dice_table_elements['part_one']:
    print(f'dobbelsteen rol: {el.row_ind + 2}, bar index: {el.get_bar_indices()[0]}')
for el in selection.dice_table_elements['part_two']:
    print(f'dobbelsteen rol: {el.row_ind + 2}, bar index: {el.get_bar_indices()[0]}')

dice_game.compile_composition_score(selection, single_page=True,
                                    comment='Test').to_file(out_dir / 'composition_pdf.ly')
auto_convert_lilypond_file(out_dir / 'composition_pdf.ly')

midi_settings = dice_game.get_default_midi_settings()
# my_midi_settings = midi_settings.with_updated_instrument('flute', 'menuet', 'piano_right_hand')

dice_game.compile_composition_audio(selection,
                                    midi_settings=midi_settings).to_file(out_dir / 'composition_midi.ly')
auto_convert_lilypond_file(
    out_dir / 'composition_midi.ly',
    soundfont=Path('/home/robbert/programming/python/opus_infinity.org/soundfonts/Musyng_Kite.sf2'))
