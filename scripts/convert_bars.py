__author__ = 'Robbert Harms'
__date__ = '2024-04-09'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import re
from pathlib import Path

from ruyaml import YAML

from musical_games.dice_games2.base import SimpleBar, Bar, SimpleSynchronousBars, SimpleBarCollection, \
    SimpleMultiVoiceBar
from musical_games.dice_games2.data_csv import SimpleBarCollectionCSVWriter

with open('/home/robbert/programming/python/musical_games/musical_games/data/dice_games/kirnberger_menuet_trio/config.yaml', 'r') as f:
    yaml = YAML().load(f)

def load_item(item: str) -> Bar:
    voices = item[3:-3].split('\\new Voice')

    if len(voices) > 1:
        voice_names_to_index = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4}
        voice_results = {}
        for voice_data in voices:
            match_groups = re.search(r"{\\voice([a-zA-Z]+) (.*)}", voice_data).groups()
            voice_results[voice_names_to_index[match_groups[0]]] = SimpleBar(match_groups[1])
        return SimpleMultiVoiceBar(voice_results)
    else:
        return SimpleBar(item)


bars_rh = yaml['game_mechanics']['bars']['trio']['piano_right_hand']
bars_lh = yaml['game_mechanics']['bars']['trio']['piano_left_hand']

sync_bars = {}
for right_hand, left_hand in list(zip(bars_rh.items(), bars_lh.items())):
    sync_bars[right_hand[0]] = SimpleSynchronousBars((load_item(right_hand[1]), load_item(left_hand[1])))

    # print(f'{right_hand[0]}: SimpleSynchronousBars((SimpleBar("{right_hand[1]}"), SimpleBar("{left_hand[1]}"))),')

a = SimpleBarCollection(sync_bars)
print()

writer = SimpleBarCollectionCSVWriter(['piano_right_hand', 'piano_left_hand'])
writer.write_csv(a, Path('/tmp/test.csv'))
