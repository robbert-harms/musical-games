from musical_games.base import MidiOptions
from musical_games.dice_games.factory import DiceGameFactory
from musical_games.utils import correct_indent, write_lilypond_book, auto_convert_lilypond_file

__author__ = 'Robbert Harms'
__date__ = "2015-12-05"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


factory = DiceGameFactory()

# print(factory.get_instruments('Kirnberger', 'Polonaise'))
# print(factory.get_composition_parts('Stadler', 'Menuet Trio'))
#
#
# def print_info_tree(factory):
#     for composer in factory.get_composers():
#         print(composer)
#
#         for composition in factory.get_compositions(composer):
#             print('\t' + composition)
#
#             instruments = factory.get_instruments(composer, composition)
#             composition_parts = factory.get_composition_parts(composer, composition)
#
#             for instr_part in zip(composition_parts, instruments):
#                 print(instr_part)
#
# print_info_tree(factory)

# composition = factory.get_composition('Stadler', 'Menuet Trio', 'Piano')
# print(composition.get_dice_tables())
# print(composition.get_composition_info())
#
# dice_tables = composition.get_dice_tables()
#
# indices = {}
# for part, tables in dice_tables.items():
#     indices.update({part: {staff_name: table.random_indices() for staff_name, table in tables.items()}})
#
# book = composition.typeset_composition(indices)
#
# write_lilypond_book('/tmp/test/composition.ly', book)
# sound_font = '/home/robbert/programming/www/opus-infinity.org/soundfonts/steinway_grand_piano.sf2'
# auto_convert_lilypond_file('/tmp/test/composition.ly', sound_font=sound_font)



# composition = factory.get_composition('Kirnberger', 'Polonaise', 'Chamber ensemble')
# composition = factory.get_composition('Mozart', 'Waltz', 'Piano')
composition = factory.get_composition('C.P.E. Bach', 'Counterpoint', 'Piano')

# book = composition.typeset_measure_overview()
# write_lilypond_book('/tmp/test/measure_overview.ly', book)
# auto_convert_lilypond_file('/tmp/test/measure_overview.ly')
#
# book = composition.parts[0].instrument.typeset_single_measure({'Right hand': 5})
# write_lilypond_book('/tmp/test/single_measure.ly', book)


dice_tables = composition.get_dice_tables()
indices = {}
for part, tables in dice_tables.items():
    indices.update({part: {staff_name: table.random_indices(0) for staff_name, table in tables.items()}})

book = composition.typeset_composition(indices)
write_lilypond_book('/tmp/test/composition.ly', book)
# sound_font = '/home/robbert/programming/www/opus-infinity.org/soundfonts/Arachno_SoundFont_Version_1.0.sf2'
# auto_convert_lilypond_file('/tmp/test/composition.ly', sound_font=sound_font)

#
#
# composition = factory.get_composition('Kirnberger', 'Menuet Trio', 'Piano')
#
# book = composition.typeset_measure_overview()
# write_lilypond_book('/tmp/test/measure_overview.ly', book)
#
# book = composition.parts[0].typeset_single_measure(5)
# write_lilypond_book('/tmp/test/single_measure.ly', book)
#
# dice_tables = composition.get_dice_tables()
# indices = {}
# for part, tables in dice_tables.items():
#     indices.update({part: [table.random_indices() for table in tables]})
#
# book = composition.typeset_composition(indices)
# write_lilypond_book('/tmp/test/composition.ly', book)
# sound_font = '/home/robbert/programming/www/opus-infinity.org/soundfonts/steinway_grand_piano.sf2'
# auto_convert_lilypond_file('/tmp/test/composition.ly', sound_font=sound_font)
