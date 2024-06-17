__author__ = 'Robbert Harms'
__date__ = '2024-04-29'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import re
from pathlib import Path

from frozendict import frozendict

from musical_games.dice_games.base import SimpleBarCollection, SimpleBar, SimpleBarSequence, \
    SimpleSynchronousBarSequence, SimpleSynchronousBar
from musical_games.dice_games.data_csv import SimpleBarCollectionCSVWriter

lilypond_input_file = '/home/robbert/Documents/projects/opus-infinity/Würfelspiele/Calegari/aria/overview.ly'
with open(lilypond_input_file, 'r') as f:
    lines = f.readlines()

chant_bars = lines[31:251]
piano_right_hand_bars = lines[263:483]
piano_left_hand_bars = lines[492:712]

def clean_bar(bar):
    if bar.strip().startswith('|'):
        return bar.strip()[1:].strip()
    return bar.strip()

sync_bars = {}
anacrusis = None
for ind, (chant_bar, piano_right_hand_bar, piano_left_hand_bar) in enumerate(zip(chant_bars,
                                                                             piano_right_hand_bars,
                                                                             piano_left_hand_bars)):
    match = re.search(r'Score\.currentBarNumber = #(\d+)', chant_bar)
    bar_index = int(match.groups()[0])

    chant_bar_clean = chant_bar[match.end()+1:].strip()
    piano_right_hand_bar_clean = clean_bar(piano_right_hand_bar)
    piano_left_hand_bar_clean = clean_bar(piano_left_hand_bar)

    current_item = SimpleSynchronousBar(frozendict({
        'chant': SimpleBar(chant_bar_clean),
        'piano_right_hand': SimpleBar(piano_right_hand_bar_clean),
        'piano_left_hand': SimpleBar(piano_left_hand_bar_clean)}))

    if bar_index == 0:
        anacrusis = current_item
    elif anacrusis is not None:
        sync_bars[bar_index] = SimpleSynchronousBarSequence((anacrusis, current_item))
        anacrusis = None
    else:
        sync_bars[bar_index] = SimpleSynchronousBarSequence((current_item,))

a = SimpleBarCollection(sync_bars)

writer = SimpleBarCollectionCSVWriter()
writer.write_csv(a, Path('/home/robbert/programming/python/musical-games/musical_games/data/dice_games/calegari_aria/bars_aria.csv'))

print()
