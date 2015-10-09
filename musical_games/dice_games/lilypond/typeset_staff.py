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

    def __init__(self, tracts_info):
        """Concatenates all bars."""
        self.tracts_info = tracts_info

    def get_staffs(self):
        staffs = []
        for tract_info in self.tracts_info:
            notes = []
            for bar in tract_info.bars:
                notes.append(self._bar_to_notes(bar))
            notes = "\n".join(notes)
            staffs.append(Staff(notes, tract_info.clef))

        return staffs

    def _bar_to_notes(self, bar):
        return str(bar)


class MozartNoRepeat(NoRepeat):
    """The no repeat listing for the Mozart Waltz.

    In the Mozart bar listing the alternative endings are superimposed on each other as two voices. We copied
    that scheme using this class.
    """
    def _bar_to_notes(self, bar):
        if bar.alternatives:
            return r'<< {\voiceOne ' + str(bar.alternatives[0]) + r'} \new Voice { \voiceTwo ' + str(bar) + '} >>'
        else:
            return str(bar)