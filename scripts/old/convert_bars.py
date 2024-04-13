__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import re
from pathlib import Path

from ruyaml import YAML

from musical_games.dice_games2.base import SimpleBar, Bar, SimpleBarCollection
from musical_games.dice_games2.data_csv import SimpleBarCollectionCSVWriter

with open('/home/robbert/programming/python/musical-games/musical_games/data/dice_games/stadler_menuet_trio/config.yaml', 'r') as f:
    yaml = YAML().load(f)


bars_rh = yaml['game_mechanics']['bars']['trio']['piano_right_hand']
bars_lh = yaml['game_mechanics']['bars']['trio']['piano_left_hand']

sync_bars = {}
for right_hand, left_hand in list(zip(bars_rh.items(), bars_lh.items())):
    sync_bars[right_hand[0]] = {'piano_right_hand': SimpleBar(right_hand[1]),
                                'piano_left_hand': SimpleBar(left_hand[1])}

a = SimpleBarCollection(sync_bars)
print(a)

writer = SimpleBarCollectionCSVWriter()
writer.write_csv(a, Path('/tmp/trio_bars.csv'))
