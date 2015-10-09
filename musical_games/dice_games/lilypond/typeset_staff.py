from musical_games.dice_games.lilypond.base import Staff

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class StaffBuilder(object):

    def get_staffs(self):
        """Get a list of Staffs to be used by the typesetter.

        Returns:
            list of Staff: list of staff objects to use during typesetting of a piece.
        """
        pass


class NoRepeat(StaffBuilder):

    def __init__(self, tracts_info, instrument_names=()):
        """Concatenate all bars behind each other."""
        self.tracts_info = tracts_info
        self.instrument_names = instrument_names

    def get_staffs(self):
        staffs = []
        for ind, tract_info in enumerate(self.tracts_info):
            instrument_name = ''
            if ind in self.instrument_names:
                instrument_name = self.instrument_names[ind]

            notes = 'g4'

            staffs.append(Staff(notes, tract_info.clef, instrument_name=instrument_name))

        return staffs