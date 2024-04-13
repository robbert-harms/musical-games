__author__ = 'Robbert Harms'
__date__ = '2024-04-12'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import csv

import pandas as pd

bars = pd.read_csv('/musical_games/data/dice_games2/cpe_bach_counterpoint/bars.csv')

bars[['bar_index', 'treble']].to_csv('/tmp/bars_treble.csv', index=False)
bars[['bar_index', 'bass']].to_csv('/tmp/bars_bass.csv', index=False)

