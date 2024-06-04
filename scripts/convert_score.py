__author__ = 'Robbert Harms'
__date__ = '2024-06-03'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import re
from pprint import pprint

import pandas as pd

from musical_games.dice_games.dice_games import CalegariAria

with open('/home/robbert/Documents/projects/opus-infinity/Würfelspiele/Calegari/aria/Cal-j1-11.ly', 'r') as f:
    lines = f.readlines()

def get_group_data():
    group_data = {}
    collect_data = False
    current_group = None
    for line in lines:
        line = line.strip()

        if line.startswith('PartP'):
            collect_data = True
            current_group = line[:line.index('=')-1]
            group_data[current_group] = []
        elif line.startswith('\score'):
            collect_data = False

        if collect_data:
            group_data[current_group].append(line)
    return group_data

def strip_ending(text):
    for ind in reversed(range(len(text))):
        if text[ind] == '}':
            return text[:ind]

def split_on_indicator(text):
    text = text.replace('\n', ' ')

    def get_bar_ind_from_group(capture_groups):
        for group in capture_groups:
            if group is not None:
                return int(group)

    bar_indices = {}
    bar_ind = []
    current_bar_ind = 1
    for match in re.finditer(r'(?:\| % (\d+))|(?:\| \\barNumberCheck #(\d+))', text):
        current_bar_ind = get_bar_ind_from_group(match.groups())

        if len(bar_ind) == 0:
            bar_ind.append(match.end())
        else:
            bar_ind.append(match.start())
            bar_indices[current_bar_ind - 1] = bar_ind
            bar_ind = [match.end()]
    bar_ind.append(len(text))
    bar_indices[current_bar_ind] = bar_ind

    bars = {}
    for bar_ind, bar_index in bar_indices.items():
        bar = text[bar_index[0]:bar_index[1]].strip()
        if bar.startswith('}'):
            bar = bar[1:].strip()
        bars[bar_ind] = bar
    return bars


def separate_bars(single_group):
    text = strip_ending('\n'.join(single_group))
    bars = split_on_indicator(text)
    return bars

def merge_voices(voices1, voices2):
    merged = {}
    for ind, bar in voices1.items():
        if ind in voices2:
            voice2_bar = voices2[ind]
            if not voice2_bar.startswith('s1'):
                merged[ind] = r'{<<{\voiceOne ' + bar + r'} \new Voice {\voiceTwo ' + voice2_bar + '}>>}'
                continue
        merged[ind] = bar
    return merged

group_data = get_group_data()

bars_per_group = {}
for key, single_group in group_data.items():
    bars_per_group[key] = separate_bars(single_group)

col = CalegariAria().get_dice_tables()['part_two'].get_column(1)
col_ind = [el.get_bar_indices()[0] for el in col]

bar_items = {'chant': bars_per_group['PartPOneVoiceOne'],
              # 'piano_right_hand': merge_voices(bars_per_group['PartPTwoVoiceOne'], bars_per_group['PartPTwoVoiceTwo']),
            'piano_right_hand': bars_per_group['PartPTwoVoiceOne'],
              'piano_left_hand': bars_per_group['PartPThreeVoiceOne']}


final_items = {}
for ind, col_el in enumerate(col_ind):
    final_items[col_el] = {'chant': bar_items['chant'][ind + 1],
                           'piano_right_hand': bar_items['piano_right_hand'][ind + 1],
                           'piano_left_hand': bar_items['piano_left_hand'][ind + 1]}

pprint(final_items)
#
# csv_f = '/home/robbert/programming/python/musical-games/musical_games/data/dice_games/calegari_aria/bars_aria.csv'
# csv_data = pd.read_csv(csv_f)
#
# for bar_index, bars in final_items.items():
#     row = csv_data[csv_data['bar_index'] == bar_index]
#     row['chant'] = 's1'
#     row['piano_right_hand'] = bars['piano_right_hand']
#     row['piano_left_hand'] = bars['piano_left_hand']
#     csv_data[csv_data['bar_index'] == bar_index] = row
#
#
# csv_data.to_csv(csv_f, index=False)
