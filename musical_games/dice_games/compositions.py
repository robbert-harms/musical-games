from musical_games.dice_games.base import PieceInfo
from musical_games.dice_games.instrumental_settings import PianoSolo, ChamberMusic

__author__ = 'Robbert Harms'
__date__ = "2015-09-19"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class Composition(object):

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

    def get_instrument_settings(self):
        """Get the types of instruments supported by this musical work.

        This differentiates between for example Piano solo and Chamber music.

        Returns:
            list of InstrumentType: the different types of instruments supported
        """


class KirnbergerMenuetTrio(Composition):

    @property
    def name(self):
        return 'Menuet / Trio'

    @property
    def safe_name(self):
        return 'menuet_trio'

    def get_instrument_settings(self):
        return [PianoSolo(), ChamberMusic()]


class KirnbergerPolonaise(Composition):

    @property
    def name(self):
        return 'Polonaise'

    @property
    def safe_name(self):
        return 'polonaise'

    def get_instrument_settings(self):
        return [PianoSolo([PieceInfo(), PieceInfo()]),
                ChamberMusic([PieceInfo(), PieceInfo()])]



class StadlerMenuetTrio(Composition):

    @property
    def name(self):
        return 'Menuet / Trio'

    @property
    def safe_name(self):
        return 'menuet_trio'

    def get_instrument_settings(self):
        return [PianoSolo([PieceInfo(), PieceInfo()])]


class MozartWaltz(Composition):

    @property
    def name(self):
        return 'Waltz'

    @property
    def safe_name(self):
        return 'waltz'

    def get_instrument_settings(self):
        return [PianoSolo([PieceInfo(), PieceInfo()])]