__author__ = 'Robbert Harms'
__date__ = '2021-03-29'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


import yaml

with open('/home/robbert/programming/python/musical-games/musical_games/data/dice_games/mozart_waltz/config.yaml') as f:
    config = yaml.safe_load(f)



print('piano_right_hand:')
for bar_nmr, staffs in config['bars']['waltz'].items():
    print(f'\t{bar_nmr}: "{staffs[0]}"')

print('piano_left_hand:')
for bar_nmr, staffs in config['bars']['waltz'].items():
    print(f'\t{bar_nmr}: "{staffs[1]}"')

print('piano_left_hand_alternative:')
for bar_nmr, staffs in config['bars']['waltz'].items():
    if len(staffs) > 2:
        print(f'\t{bar_nmr}: "{staffs[2]}"')
    else:
        print(f'\t{bar_nmr}: ')
