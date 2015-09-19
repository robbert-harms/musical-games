__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class InstrumentalSetting(object):

    def __init__(self, pieces_info):
        """Information about the instrumental settings for a composition.

        Args:
            measures (list of PieceInfo): information about the pieces to be used by this instrumental setting
        """
        self.pieces_info = pieces_info

    @property
    def name(self):
        """Returns the name of this work.

        Returns:
            str: the name of this work
        """
        return ''

    @property
    def safe_name(self):
        """Get a safe name of this work. This should only contain alphanumeric signs and underscore.

        Returns:
            str: the safe name of this work.
        """
        return ''


class PianoSolo(InstrumentalSetting):

    @property
    def name(self):
        return 'Piano solo'

    @property
    def safe_name(self):
        return 'piano'


class ChamberMusic(InstrumentalSetting):

    @property
    def name(self):
        return 'Chamber music'

    @property
    def safe_name(self):
        return 'chamber_music'
