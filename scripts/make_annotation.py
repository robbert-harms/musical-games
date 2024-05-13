__author__ = 'Robbert Harms'
__date__ = '2024-05-13'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import csv
import json

csv_in = '/home/robbert/programming/python/musical-games/musical_games/data/dice_games/gerlach_scottish_dance/scottish_dance_bars.csv'
csv_out = '/home/robbert/programming/python/musical-games/musical_games/data/dice_games/gerlach_scottish_dance/scottish_dance_bars_annotations.csv'


output_rows = [('bar_index', 'piano_right_hand', 'piano_left_hand')]
with open(csv_in, 'r', newline='') as csvfile:
    bar_reader = csv.reader(csvfile, dialect='unix')

    for row in list(bar_reader)[1:]:
        if 'treble' in row[2]:
            annotation = {'clef': 'treble'}
        elif 'bass' in row[2]:
            annotation = {'clef': 'bass'}
        else:
            annotation = ''

        output_rows.append((row[0], '', json.dumps(annotation)))


with open(csv_out, 'w', newline='') as csvfile:
    bar_writer = csv.writer(csvfile, dialect='unix')

    for output_row in output_rows:
        bar_writer.writerow(output_row)
