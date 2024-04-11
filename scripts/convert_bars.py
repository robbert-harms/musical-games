__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


from ruyaml import YAML

with open('/home/robbert/programming/python/musical-games/musical_games/data/dice_games/cpe_bach_counterpoint/config.yaml', 'r') as f:
    yaml = YAML().load(f)

right = yaml['game_mechanics']['bars']['treble']['piano_right_hand']
left = yaml['game_mechanics']['bars']['bass']['piano_left_hand']


for right_hand, left_hand in list(zip(right.items(), left.items())):
    print(f'{right_hand[0]}: SimpleSynchronousBars((SimpleBar("{right_hand[1]}"), SimpleBar("{left_hand[1]}"))),')

