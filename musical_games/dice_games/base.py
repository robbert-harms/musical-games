__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class PieceInfo(object):

    def __init__(self, measures, key_signature, time_signature, tempo):
        self.measures = measures
        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo = tempo